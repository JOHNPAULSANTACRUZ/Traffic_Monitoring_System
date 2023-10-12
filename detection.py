import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np

model = YOLO('/weights/yolov8n.pt')


# def bounding_box(coordinates_array):
#     global ZONE_POLYGON
#     ZONE_POLYGON = np.array(coordinates_array)
#     return ZONE_POLYGON


# This function will generate frames and will be called by app.py

def gen_frames():
    cap = cv2.VideoCapture(camera_id)

    box_annotator = sv.BoxAnnotator(
        thickness=1,
        text_thickness=1,
        text_scale=1
    )

    # bounding box draw
    # zone_polygon = (ZONE_POLYGON * np.array([640, 480])).astype(int)
    # zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=(640, 480))
    # zone_annotator = sv.PolygonZoneAnnotator(
    #     zone=zone,
    #     color=sv.Color.red(),
    #     thickness=2,
    #     text_thickness=4,
    #     text_scale=2
    # )

    # loop detection
    while True:
        ret, frame = cap.read()

        # Check if the video has reached the end
        if not ret:
            # Set the position of the video back to the start
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        # labels = [
        #     f"{model.model.names[class_id]} {confidence:0.2f}"
        #     for _, confidence, class_id, _
        #     in detections
        # ]
        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            # labels=labels
        )

        # zone.trigger(detections=detections)
        # frame = zone_annotator.annotate(scene=frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
