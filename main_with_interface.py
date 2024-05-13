import argparse

import cv2

from ultralytics import YOLO

import supervision as sv
import numpy as np

import torch

print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))


def draw_line(x1, y1, x2, y2, nr_of_line, image, thickness):
    start_point = (x1, y1)

    # represents the bottom right corner of image
    end_point = (x2, y2)

    # Green color in BGR
    if nr_of_line == 0 or nr_of_line == 1:
        color = (0, 0, 255)
    elif nr_of_line == 2 or nr_of_line == 3:
        color = (0, 128, 255)
    elif nr_of_line >= 4:
        color = (0, 255, 0)

    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 9 px
    frame = cv2.line(image, start_point, end_point, color, thickness)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution", default=[1920, 1080], nargs=2, type=int)
    args = parser.parse_args()
    return args


def main(chk_car, chk_person, chk_bollard, crop_x1, crop_x2, crop_y1, crop_y2, offset, nr_of_lines, space_between_lines,
         angle_of_lines):
    # define a video capture object
    args = parse_arguments()
    video_path = "videos/2024-04-17 17-42-13.mp4"
    vid = cv2.VideoCapture(video_path)

    model = YOLO("best.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    while True:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        frame = frame[crop_y1:crop_y2, crop_x1:crop_x2]

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)

        # bollard - 0
        # car - 1
        # person - 2

        selected_classes = []

        if chk_bollard:
            selected_classes.append(0)

        if chk_car:
            selected_classes.append(1)

        if chk_person:
            selected_classes.append(2)

        detections = detections[np.isin(detections.class_id, selected_classes)]

        labels = []
        for element in detections:
            label = f"{model.model.names[element[2]]}, {element[1]:0.2f}"
            labels.append(label)

        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

        # space_between_lines = 100
        start_draw_lines_y = crop_y2
        # modify for height:
        end_draw_lines_y = start_draw_lines_y - nr_of_lines * space_between_lines

        height_of_line = crop_y2
        left_edge_x = 50
        right_edge_x = 100

        # modify for width:
        # offset = 725
        middle = int(abs(crop_x2 - crop_x1) / 2)
        middle_line_left_x = middle - offset
        middle_line_right_x = middle + offset
        nr_of_line = 0

        const = 150
        start_drawing_bottom_left = middle_line_left_x + const
        start_drawing_bottom_right = middle_line_right_x - const

        # Line thickness of 9 px
        thickness = 9

        # draw lines on camera
        for i in range(start_draw_lines_y, end_draw_lines_y, -space_between_lines):
            # draw left edge line
            draw_line(start_drawing_bottom_left, height_of_line, middle_line_left_x, i, nr_of_line, frame, thickness)

            # draw right edge line
            draw_line(start_drawing_bottom_right, height_of_line, middle_line_right_x, i, nr_of_line, frame, thickness)

            height_of_line = i
            start_drawing_bottom_left = middle_line_left_x
            start_drawing_bottom_right = middle_line_right_x

            # draw middle line from left
            draw_line(middle_line_left_x, i, middle_line_left_x + 100, i, nr_of_line, frame, thickness)

            # draw middle line from right
            draw_line(middle_line_right_x, i, middle_line_right_x - 100, i, nr_of_line, frame, thickness)

            nr_of_line += 1

            # modify for angle of lines:
            # angle_of_lines = 110
            middle_line_left_x += angle_of_lines
            middle_line_right_x -= angle_of_lines

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
