import base64
import mimetypes
import cv2
def create_image_message(image_path):
    # Open the image file in "read binary" mode
    with open(image_path, "rb") as image_file:
        # Read the contents of the image as a bytes object
        binary_data = image_file.read()
    
    # Encode the binary data using Base64 encoding
    base64_encoded_data = base64.b64encode(binary_data)
    
    # Decode base64_encoded_data from bytes to a string
    base64_string = base64_encoded_data.decode('utf-8')
    
    # Get the MIME type of the image based on its file extension
    mime_type, _ = mimetypes.guess_type(image_path)
    
    # Create the image block
    image_block = {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": base64_string
        }
    }
    
    
    return image_block

def get_frames_from_video(file_path, max_images=20):
    video = cv2.VideoCapture(file_path)
    base64_frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpeg", frame)
        base64_frame = base64.b64encode(buffer).decode("utf-8")
        base64_frames.append(base64_frame)
    video.release()
    # Limit the number of selected images
    selected_frames = base64_frames[0::len(base64_frames)//max_images][:max_images]
    return selected_frames

def create_video_message(video_path, max_images=20):
    base64_frames = get_frames_from_video(video_path, max_images)
    return [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": frame}} for frame in base64_frames]

