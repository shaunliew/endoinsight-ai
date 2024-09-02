from config import *
from helper import *

def process_video(video_path, prompt, yolo_model_path, model=MODEL_TYPE, max_images=20, conf_threshold=0.8):
    # Get total frame count
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    # Calculate frame indices to sample
    if total_frames <= max_images:
        frame_indices = list(range(total_frames))
    else:
        frame_indices = [int(i * (total_frames - 1) / (max_images - 1)) for i in range(max_images)]

    # Process video with YOLO
    yolo_results = process_video_with_yolo(video_path, yolo_model_path, conf_threshold)

    # Create video message for selected frames
    video_blocks = create_video_message(video_path, max_images, frame_indices)

    labeled_content = []
    for i, (block, frame_index) in enumerate(zip(video_blocks, frame_indices), start=1):
        yolo_frame = yolo_results[frame_index]
        yolo_detections = []
        for detection in yolo_frame['detections']:
            yolo_detections.append(f"Class: {detection['class']}, Confidence: {detection['confidence']:.2f}, {detection['mask_description']}")
        
        labeled_content.extend([
            {"type": "text", "text": f"Frame {frame_index + 1} of {total_frames}:"},
            block,
            {"type": "text", "text": f"YOLO Detections: {'; '.join(yolo_detections)}"}
        ])
    
    labeled_content.append({
        "type": "text",
        "text": prompt
    })
    
    message_list = [
        {
            "role": "user",
            "content": labeled_content,
        }
    ]

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=message_list,
        temperature=0.05,
    )

    return response.content[0].text

if __name__ == "__main__":
    video_file_path = "test/video.mp4"
    yolo_model_path = "weights/trained_model.pt"
    result = process_video(video_file_path, VIDEO_INSTRUCTION_PROMPT, yolo_model_path)
    print(result)