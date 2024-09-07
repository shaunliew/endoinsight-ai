import base64
import cv2
from ultralytics import YOLO
import numpy as np
import torch
from typing import Dict, Tuple, NamedTuple
from google.cloud import storage

def create_video_message(video_path, max_images=20, frame_indices=None):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_indices is None:
        if total_frames <= max_images:
            frame_indices = list(range(total_frames))
        else:
            frame_indices = [int(i * (total_frames - 1) / (max_images - 1)) for i in range(max_images)]

    video_blocks = []
    for frame_index in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            base64_image = base64.b64encode(buffer).decode('utf-8')
            video_blocks.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_image
                }
            })

    cap.release()
    return video_blocks

class ColorClass(NamedTuple):
    color: Tuple[int, int, int]
    name: str

class SegmentationClasses:
    def __init__(self):
        # the colour scheme is given based on the documentation
        self.class_info: Dict[int, ColorClass] = {
            0: ColorClass((127, 127, 127), 'Black Background'),
            1: ColorClass((210, 140, 140), 'Abdominal Wall'),
            2: ColorClass((255, 114, 114), 'Liver'),
            3: ColorClass((231, 70, 156), 'Gastrointestinal Tract'),
            4: ColorClass((186, 183, 75), 'Fat'),
            5: ColorClass((170, 255, 0), 'Grasper'),
            6: ColorClass((255, 85, 0), 'Connective Tissue'),
            7: ColorClass((255, 0, 0), 'Blood'),
            8: ColorClass((255, 255, 0), 'Cystic Duct'),
            9: ColorClass((169, 255, 184), 'L-hook Electrocautery'),
            10: ColorClass((255, 160, 165), 'Gallbladder'),
            11: ColorClass((0, 50, 128), 'Hepatic Vein'),
            12: ColorClass((111, 74, 0), 'Liver Ligament')
        }
        
        self.color_to_class: Dict[Tuple[int, int, int], int] = {
            info.color: class_index for class_index, info in self.class_info.items()
        }
        
        self.name_to_class: Dict[str, int] = {
            info.name: class_index for class_index, info in self.class_info.items()
        }
    
    def get_class_from_color(self, color: Tuple[int, int, int]) -> int:
        return self.color_to_class.get(color, -1)  # Returns -1 if color not found
    
    def get_color_from_class(self, class_index: int) -> Tuple[int, int, int]:
        return self.class_info[class_index].color if class_index in self.class_info else (0, 0, 0)
    
    def get_name_from_class(self, class_index: int) -> str:
        return self.class_info[class_index].name if class_index in self.class_info else "Unknown"
    
    def get_class_from_name(self, name: str) -> int:
        return self.name_to_class.get(name, -1)  # Returns -1 if name not found
    
    def get_color_name(self, class_index: int) -> str:
        if class_index in self.class_info:
            color = self.class_info[class_index].color
            return f"RGB{color}"
        return "Unknown"

def process_video_with_yolo(video_path, yolo_model_path, output_path, conf_threshold=0.8):
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = YOLO(yolo_model_path)
    model.to(device)
    
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    segmentation_results = {}
    frame_count = 0

    seg_classes = SegmentationClasses()

    def adjust_label_position(frame, label, top, left, font, font_scale, font_thickness):
        (label_width, label_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)
        
        if left + label_width > frame_width:
            left = frame_width - label_width
        
        if top - label_height - baseline < 0:
            top = label_height + baseline
        
        return top, left, font_scale

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=conf_threshold, device=device)[0]
        frame_results = []

        if results.masks is not None:
            full_mask = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

            for seg, box, cls in zip(results.masks.data, results.boxes.data, results.boxes.cls):
                class_index = int(cls)
                class_name = seg_classes.get_name_from_class(class_index)
                # Skip the "Black Background" class
                if class_name == "Black Background":
                    continue
                confidence = float(box[4])
                
                mask = (seg.cpu().numpy() > 0.5).astype(np.uint8)
                mask = cv2.resize(mask, (frame_width, frame_height), interpolation=cv2.INTER_NEAREST)

                area = np.sum(mask)
                y, x = np.where(mask)
                if len(y) > 0 and len(x) > 0:
                    top, left = np.min(y), np.min(x)
                    bottom, right = np.max(y), np.max(x)
                    height, width = bottom - top, right - left
                    center_y, center_x = (top + bottom) // 2, (left + right) // 2

                    rel_center_y = center_y / frame_height
                    rel_center_x = center_x / frame_width

                    aspect_ratio = width / height if height != 0 else 0
                    frame_coverage = area / (frame_width * frame_height)

                    if rel_center_y < 0.33:
                        vertical_pos = "upper"
                    elif rel_center_y < 0.66:
                        vertical_pos = "middle"
                    else:
                        vertical_pos = "lower"

                    if rel_center_x < 0.33:
                        horizontal_pos = "left"
                    elif rel_center_x < 0.66:
                        horizontal_pos = "center"
                    else:
                        horizontal_pos = "right"

                    general_pos = f"{vertical_pos} {horizontal_pos}"

                    mask_description = (
                        f"Object: {class_name}, Confidence: {confidence:.2f}, "
                        f"Position: {general_pos} of the frame, "
                        f"Bounding Box: top-left ({top}, {left}), bottom-right ({bottom}, {right}), "
                        f"Relative Position: center ({rel_center_x:.2f}, {rel_center_y:.2f}), "
                        f"Size: {width}x{height} pixels, Area: {area} pixels, "
                        f"Frame Coverage: {frame_coverage:.2%}, "
                        f"Aspect Ratio: {aspect_ratio:.2f}"
                    )

                    frame_results.append({
                        "class": class_name,
                        "confidence": confidence,
                        "mask_description": mask_description
                    })

                    color = seg_classes.get_color_from_class(class_index)
                    colored_mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2) * np.array(color).reshape(1, 1, 3)
                    full_mask = cv2.addWeighted(full_mask, 1, colored_mask.astype(np.uint8), 0.5, 0)

                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    
                    label = f"{class_name} {confidence:.2f}"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.6
                    font_thickness = 1
                    top, left, font_scale = adjust_label_position(frame, label, top, left, font, font_scale, font_thickness)
                    
                    (label_width, label_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)
                    cv2.rectangle(frame, (left, top - label_height - baseline), (left + label_width, top), color, -1)
                    
                    # Use white text for better contrast
                    cv2.putText(frame, label, (left, top - baseline), font, font_scale, (255, 255, 255), font_thickness)

            frame = cv2.addWeighted(frame, 1, full_mask, 0.5, 0)

        segmentation_results[frame_count] = {
            "frame": frame_count,
            "detections": frame_results
        }

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    return segmentation_results

def upload_video_to_gcs(bucket_name, video_data, video_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    # Create a blob object to represent the video file in the bucket
    blob = bucket.blob(video_path)
    
    # Upload the video file to the bucket
    blob.upload_from_string(video_data, content_type="video/mp4")
    
    # Make the blob publicly accessible
    blob.make_public()
    
    # Get the public URL
    video_url = blob.public_url
    return video_url
