import argparse

import cv2

from ultralytics import YOLO

import supervision as sv
import numpy as np

import torch

print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))

# ZONE_POLYGON = np.array([
#     [0, 0],
#     [1920 // 2, 0],
#     [1920 // 2, 1080],
#     [0, 1080]
# ])


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution", default=[1920, 1080], nargs=2, type=int)
    args = parser.parse_args()
    return args


# define a video capture object
args = parse_arguments()
frame_width, frame_height = args.webcam_resolution
video_path = "videos/2024-04-17 17-42-13.mp4"
vid = cv2.VideoCapture(video_path)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

model = YOLO("best.pt")

box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=2,
    text_scale=1
)

# zone = sv.PolygonZone(polygon=ZONE_POLYGON, frame_resolution_wh=tuple(args.webcam_resolution))
# zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.red(), thickness=2, text_thickness=4, text_scale=2)

while True:
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    result = model(frame, agnostic_nms=True)[0]
    detections = sv.Detections.from_yolov8(result)
    # detections = detections[detections.class_id != 0]

    labels = []
    for _, confidence, class_id, _ in detections:
        # if model.model.names[class_id] == "car" or model.model.names[class_id] == "person":
        label = f"{model.model.names[class_id]}, {confidence:0.2f}"
        labels.append(label)

    frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

    # zone.trigger(detections=detections)
    # frame = zone_annotator.annotate(scene=frame)

    cv2.imshow('frame', frame)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
