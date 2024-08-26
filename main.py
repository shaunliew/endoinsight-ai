from config import *
from helper import *

# get the local image
image_path = "dataset/video01/video01_16345/frame_16345_endo.png"

image_block = create_image_message(image_path)

message_list = [
        {
            "role": "user",
            "content": [
                image_block,
                {
                    "type": "text",
                    "text": INSTRUCTION_PROMPT
                }
            ],
        }
    ]

response = client.messages.create(
    model=MODEL_TYPE,
    max_tokens=1024,
    system = SYSTEM_PROMPT,
    messages=message_list,
    temperature=0.05,
)

print(response.content[0].text)