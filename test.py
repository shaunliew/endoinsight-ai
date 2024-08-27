from ultralytics import YOLO

# Load a model
model = YOLO("weights/yolov8n-seg.pt")  # load an official model

# Predict with the model
results = model("test/video.mp4", save=True, project="/Users/shaunliew/Documents/endoinsight-ai/runs")  # predict on an image