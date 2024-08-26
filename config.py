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