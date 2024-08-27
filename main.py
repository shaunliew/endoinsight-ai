from config import *
from helper import *

def process_video(video_path, prompt, model=MODEL_TYPE, max_images=20):
    video_blocks = create_video_message(video_path, max_images)
    
    labeled_content = []
    for i, block in enumerate(video_blocks, start=1):
        labeled_content.extend([
            {"type": "text", "text": f"Frame {i}:"},
            block
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
    result = process_video(video_file_path, VIDEO_INSTRUCTION_PROMPT)
    print(result)

    # image_path = "dataset/video01/video01_16345/frame_16345_endo.png"
    # image_block = create_image_message(image_path)

    # message_list = [
    #         {
    #             "role": "user",
    #             "content": [
    #                 image_block,
    #                 {
    #                     "type": "text",
    #                     "text": INSTRUCTION_PROMPT
    #                 }
    #             ],
    #         }
    #     ]

    # response = client.messages.create(
    #     model=MODEL_TYPE,
    #     max_tokens=1024,
    #     system = SYSTEM_PROMPT,
    #     messages=message_list,
    #     temperature=0.05,
    # )

    # print(response.content[0].text)