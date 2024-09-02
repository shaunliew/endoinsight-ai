import base64
import cv2
from ultralytics import YOLO
import numpy as np
import torch

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

def process_video_with_yolo(video_path, yolo_model_path, conf_threshold=0.8):
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = YOLO(yolo_model_path)
    model.to(device)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    segmentation_results = {}
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = model(frame, conf=conf_threshold, device=device)[0]
        frame_results = []

        if results.masks is not None:
            for seg, box, cls in zip(results.masks.data, results.boxes.data, results.boxes.cls):
                class_name = results.names[int(cls)]
                confidence = float(box[4])
                
                # Convert segmentation mask to binary
                mask = (seg.cpu().numpy() > 0.5).astype(np.uint8)
                
                # Calculate mask properties
                area = np.sum(mask)
                y, x = np.where(mask)
                top, left = np.min(y), np.min(x)
                bottom, right = np.max(y), np.max(x)
                height, width = bottom - top, right - left
                center_y, center_x = (top + bottom) // 2, (left + right) // 2

                # Calculate relative positions
                rel_center_y = center_y / frame_height
                rel_center_x = center_x / frame_width

                # Calculate aspect ratio and coverage
                aspect_ratio = width / height if height != 0 else 0
                frame_coverage = area / (frame_width * frame_height)

                # Determine general position
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

        segmentation_results[frame_count] = {
            "frame": frame_count,
            "detections": frame_results
        }

        frame_count += 1

    cap.release()
    return segmentation_results