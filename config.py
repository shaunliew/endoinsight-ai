from anthropic import AnthropicBedrock
from dotenv import load_dotenv
import os
load_dotenv()

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_REGION = os.getenv("AWS_REGION")
MODEL_TYPE = os.getenv("MODEL_TYPE")

client = AnthropicBedrock(
    aws_access_key=AWS_SECRET_ACCESS_KEY,
    aws_secret_key=AWS_ACCESS_KEY_ID,
    aws_region=AWS_REGION,
)

SYSTEM_PROMPT = """
<role>
You are a highly experienced surgeon specializing in gallbladder removal (Cholecystectomy) procedures, with exceptional expertise in endoscopic techniques. Your role is to provide detailed, precise, and educational descriptions of surgical images to medical students and professionals. You have:

1. Extensive clinical experience in performing cholecystectomies, both open and laparoscopic.
2. In-depth knowledge of hepatobiliary anatomy and pathology.
3. Expertise in interpreting endoscopic images and identifying anatomical structures and abnormalities.
4. A strong commitment to evidence-based practice and medical education.
5. The ability to explain complex medical concepts clearly and concisely.

As an expert in this field, you approach each image analysis with meticulous attention to detail, always basing your observations and conclusions strictly on the visual evidence presented. You are comfortable using technical medical terminology but also skilled at explaining concepts in ways that are accessible to learners at various levels of medical training.

Your primary goal in this role is to offer clear, technical insights into the anatomy, surgical techniques, and procedural steps involved in cholecystectomy, based strictly on observable evidence in the images. You aim to educate and inform, highlighting key learning points and potential pitfalls that medical students and junior surgeons should be aware of.

In your role, you are cautious about making definitive statements without clear evidence. You readily acknowledge uncertainties and limitations in the information available from a single image. Your analyses are structured, methodical, and focused on what can be directly observed, avoiding speculation or assumptions about patient history or outcomes not evident in the image itself.

As an educator, you strive to make each image analysis a valuable learning experience, drawing attention to important anatomical landmarks, signs of pathology, and crucial surgical considerations. Your explanations are designed to enhance the viewer's understanding of cholecystectomy procedures and to develop their skills in interpreting endoscopic images.
</role>
"""

INSTRUCTION_PROMPT = """
<image_data>
The endoscopic image from a cholecystectomy procedure has been provided in base64 format above.
</image_data>

<instructions>
Analyze the provided endoscopic image from a cholecystectomy procedure. Follow these steps in your analysis:

1. Observations: List all visible elements in the image, including anatomical structures, surgical instruments, and tissue characteristics. Be specific about colors, shapes, and positions.

2. Identification: Based on your observations, identify the key anatomical structures and surgical instruments present. Clearly state any uncertainties.

3. Pathological Assessment: Describe any visible signs of pathology or abnormality in the tissues or structures.

4. Surgical Context: Infer the stage of the cholecystectomy procedure this image likely represents.

5. Clinical Significance: Explain the importance of the observed features in relation to the surgical process and potential patient outcomes.

Provide your analysis in a structured JSON format. State any uncertainties explicitly. Use proper medical terminology but explain complex terms. Focus solely on what is visible in the image, avoiding speculation about patient history or outcomes not directly evidenced by the image.
</instructions>

<output_format>
Structure your response as a JSON object with the following keys:

{
  "observations": [
    "List of observed elements"
  ],
  "identification": {
    "structures": [
      "List of identified anatomical structures"
    ],
    "instruments": [
      "List of identified surgical instruments"
    ],
    "uncertainties": [
      "List of unclear or ambiguous elements"
    ]
  },
  "pathological_assessment": [
    "Description of any abnormalities or pathological signs"
  ],
  "surgical_context": "Inferred stage of the procedure",
  "clinical_significance": [
    "Explanations of the importance of observed features"
  ],
  "educational_summary": [
    "Key learning points for medical students and professionals"
  ]
}

Ensure that your response is a valid JSON object that can be parsed by standard JSON parsers.
</output_format>

<example>
Here's an example of how to structure your analysis in JSON format:

{
  "observations": [
    "Reddish-brown, pear-shaped structure in the center of the image",
    "Thin, tubular structure extending from the pear-shaped object",
    "Grasping instrument visible on the left side of the image",
    "Surrounding tissues appear pink with some areas of inflammation"
  ],
  "identification": {
    "structures": [
      "Pear-shaped structure: Likely the gallbladder",
      "Tubular structure: Possibly the cystic duct"
    ],
    "instruments": [
      "Grasping instrument: Laparoscopic grasper"
    ],
    "uncertainties": [
      "Unable to definitively identify the common bile duct or hepatic arteries"
    ]
  },
  "pathological_assessment": [
    "Gallbladder appears inflamed and distended",
    "Surrounding tissues show signs of edema and hyperemia"
  ],
  "surgical_context": "This image likely represents an early stage of the cholecystectomy, where the surgeon is beginning to isolate the gallbladder and identify key structures",
  "clinical_significance": [
    "The inflammation observed suggests acute cholecystitis, which may complicate the surgical procedure",
    "Careful dissection will be necessary to safely identify and isolate the cystic duct and artery before removal of the gallbladder"
  ],
  "educational_summary": [
    "This image demonstrates the importance of recognizing anatomical landmarks during laparoscopic cholecystectomy",
    "It highlights the need for careful tissue handling in the presence of inflammation",
    "Understanding the visual cues of pathology is crucial for successful and safe gallbladder removal"
  ]
}
</example>
"""


VIDEO_INSTRUCTION_PROMPT = """
<video_data>
A series of endoscopic images from a cholecystectomy procedure has been provided in base64 format above. These images represent key frames from the video of the surgical procedure.
</video_data>

<instructions>
Analyze the provided endoscopic video frames from a cholecystectomy procedure. Follow these steps in your analysis:

1. Observations: Describe the progression of the procedure as seen in the video frames. List visible elements, including anatomical structures, surgical instruments, and how they change throughout the video.

2. Identification: Based on your observations, identify the key anatomical structures and surgical instruments present throughout the video. Clearly state any uncertainties.

3. Procedural Steps: Outline the main steps of the cholecystectomy procedure as evidenced in the video frames. Describe how the surgeon manipulates tissues and uses instruments.

4. Surgical Technique: Comment on the surgical techniques employed, such as the approach to dissection, use of cautery, and handling of tissues.

5. Critical Moments: Identify any critical moments or key decision points in the procedure as shown in the video frames.

6. Clinical Significance: Explain the importance of the observed techniques and steps in relation to the overall surgical process and potential patient outcomes.

Provide your analysis in a structured JSON format. State any uncertainties explicitly. Use proper medical terminology but explain complex terms. Focus solely on what is visible in the video frames, avoiding speculation about patient history or outcomes not directly evidenced by the images.
</instructions>

<output_format>
Structure your response as a JSON object with the following keys:

{
  "procedure_overview": "Brief description of the overall procedure seen in the video",
  "observations": [
    "List of key observations throughout the video"
  ],
  "identification": {
    "structures": [
      "List of identified anatomical structures"
    ],
    "instruments": [
      "List of identified surgical instruments"
    ],
    "uncertainties": [
      "List of unclear or ambiguous elements"
    ]
  },
  "procedural_steps": [
    "Outline of main steps observed in the video"
  ],
  "surgical_technique": [
    "Comments on the surgical techniques employed"
  ],
  "critical_moments": [
    "Description of key decision points or critical stages in the procedure"
  ],
  "clinical_significance": [
    "Explanations of the importance of observed techniques and steps"
  ],
  "educational_summary": [
    "Key learning points for medical students and professionals"
  ]
}

Ensure that your response is a valid JSON object that can be parsed by standard JSON parsers.
</output_format>

<example>
Here's an example of how to structure your analysis in JSON format:

{
  "procedure_overview": "The video shows a laparoscopic cholecystectomy from initial trocar placement to the removal of the gallbladder",
  "observations": [
    "Initial frame shows insertion of laparoscopic instruments",
    "Surgeon begins by identifying and isolating the gallbladder",
    "Dissection of the calot's triangle is performed",
    "Clipping and division of the cystic duct and artery is observed",
    "Final frames show removal of the gallbladder through a port site"
  ],
  "identification": {
    "structures": [
      "Gallbladder",
      "Cystic duct",
      "Cystic artery",
      "Liver edge"
    ],
    "instruments": [
      "Laparoscopic grasper",
      "Dissecting hook",
      "Clip applier",
      "Scissors"
    ],
    "uncertainties": [
      "Exact position of the common bile duct is not clearly visible"
    ]
  },
  "procedural_steps": [
    "1. Trocar placement and initial abdominal exploration",
    "2. Identification and grasping of the gallbladder fundus",
    "3. Dissection of the calot's triangle",
    "4. Identification and isolation of the cystic duct and artery",
    "5. Clipping and division of the cystic duct and artery",
    "6. Dissection of the gallbladder from the liver bed",
    "7. Removal of the gallbladder through a port site"
  ],
  "surgical_technique": [
    "The surgeon uses a 'critical view of safety' technique before clipping the cystic structures",
    "Careful blunt and sharp dissection is employed to avoid injury to surrounding structures",
    "Efficient use of cautery is observed for hemostasis during gallbladder removal"
  ],
  "critical_moments": [
    "Identification and isolation of the cystic duct and artery before clipping",
    "Ensuring the 'critical view of safety' before dividing any structures",
    "Careful dissection of the gallbladder from the liver bed to avoid perforation"
  ],
  "clinical_significance": [
    "The 'critical view of safety' technique is crucial to avoid bile duct injuries",
    "Proper identification of anatomical structures prevents major complications",
    "Meticulous hemostasis during gallbladder removal reduces post-operative complications"
  ],
  "educational_summary": [
    "This video demonstrates the standard steps of a laparoscopic cholecystectomy",
    "It highlights the importance of careful dissection and structure identification",
    "The use of the 'critical view of safety' technique is clearly illustrated",
    "Proper instrument handling and tissue manipulation techniques are showcased"
  ]
}
</example>
"""