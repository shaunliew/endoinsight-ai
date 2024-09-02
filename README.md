# EndoInsight AI

AI-Powered Cholecystectomy Surgeries Video Analysis and Explanation System

## Features

### 1. Video Ingestion & Frame Extraction

- Description: Load endoscopic video files and extract key frames for further analysis.

- Tools: OpenCV for frame extraction.

### 2. Visual Feature Extraction by Object Segmentation with YOLOv8

- Description: Analyze each frame using YOLOv8 to perform object segmentation, identifying the classes of objects in the endoscopic images.

- Tools: [YOLOv8 Segmentation](https://docs.ultralytics.com/tasks/segment/)

### 3. Visual Feature Extraction

- Description: Extract relevant features from the YOLOv8 segmentation results, including object locations, sizes, and classifications.

- Tools: Custom Python scripts for feature extraction from YOLOv8 outputs
  
### 4. Textual Explanation Generation

- Description: Generate detailed textual explanations of the medical images based on the YOLOv8 segmentation results and extracted features.
  
- Tools: [Amazon Bedrock Claude 3 Haiku](https://aws.amazon.com/bedrock/claude/)

### 5. Multimodal Integration

- Description: Combine visual segmentation data and generated textual explanations to produce a contextually rich output that reflects both the visual content and the corresponding text.

- Tools: Custom scripts to align visual and textual data

### 6. Result Visualization

- Description: Generate a final output that presents the original image, YOLOv8 segmentation results, and textual explanations in an integrated format.

- Tools: Matplotlib or similar visualization libraries

### 7. User Interface (UI)

- Description: Develop a simple web interface for uploading images, running analyses, and viewing the integrated image-text output. Users should be able to interact with both the image and the generated text.

- Tools: Streamlit


## Setup GCP Credentials

get service account JSON from GCP Project in order to use GCP Service.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="gcp-credential.json"
```

## Connect GCS to Vertex AI

```bash
MY_BUCKET=endoinsight-ai
cd ~/
gcsfuse --implicit-dirs --rename-dir-limit=100 --max-conns-per-host=100 $MY_BUCKET "/home/jupyter/endoinsight-ai/gcs"
```
