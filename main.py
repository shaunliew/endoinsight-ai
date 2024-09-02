from fastapi import FastAPI, File, UploadFile, status, APIRouter
from fastapi.responses import JSONResponse
import shutil
import os
import json
from config import *
from helper import *
import uuid

app = FastAPI()

# Create an APIRouter
api_router = APIRouter()

@app.get("/")
async def root():
    return {"message": "Welcome to the Video Processing API", "status": "operational"}


def process_video(video_path, prompt, yolo_model_path, output_path, model=MODEL_TYPE, max_images=20, conf_threshold=0.8):
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
    yolo_results = process_video_with_yolo(video_path, yolo_model_path, output_path, conf_threshold)

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

@api_router.post("/process_video/")
async def process_video_endpoint(file: UploadFile = File(...)):
    # Create a unique filename for the input and output videos
    generated_uuid = uuid.uuid4()
    input_filename = f"{generated_uuid}.mp4"
    output_filename = f"{generated_uuid}_output.mp4"
    
    input_path = f"uploads/{input_filename}"
    output_path = f"output/{output_filename}"
    
    # Ensure directories exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Save the uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Process the video
        yolo_model_path = "weights/trained_model.pt"
        result = process_video(input_path, VIDEO_INSTRUCTION_PROMPT, yolo_model_path, output_path)

        # Parse the result string into a JSON object
        result_json = json.loads(result)

        # Prepare the content of the response
        content = {
            "analysis_result": result_json,
            "input_video_path": input_path,
            "output_video_path": output_path
        }

        # Return the response in the new format
        return JSONResponse(
            content={
                "success": True,
                "message": f"Video {input_filename} processed successfully.",
                "content": content
            },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        # Return an error response in the new format
        return JSONResponse(
            content={
                "success": False,
                "message": f"Error processing video: {str(e)}",
                "content": None
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Include the router with a prefix
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)