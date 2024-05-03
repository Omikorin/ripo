import math

import cv2
import numpy as np
from ultralytics import YOLO


def calculate_focal_length(AFOV_deg, SENSOR_W, SENSOR_H):
    # Convert AFOV from degrees to radians
    AFOV_rad = math.radians(AFOV_deg)

    # Calculate focal length
    focal_length = (SENSOR_W / 2) / math.tan(AFOV_rad / 2)

    # Adjust focal length based on sensor aspect ratio
    focal_length *= (SENSOR_H / SENSOR_W)

    return focal_length


# Assuming we have height, width of sensor and deg AFOV!!!

AFOV_DEG = 30  # Angular Field Of View
SENSOR_W, SENSOR_H = 23.6, 15.7  # szerokosc, wysokosc w milimetrach
SENSOR_D = math.sqrt(23.6 ** 2 + 15.7 ** 2)  # przekatna
# LENS_FOCAL = calculate_focal_length(AFOV_DEG, SENSOR_W, SENSOR_H)  # ogniskowa obiektywu
LENS_FOCAL = 40
CAMERA_POS_HEIGHT = 1.5  # wysokosc umieszczenia kamery w metrach

AFOV_HORIZONTAL = math.degrees(2 * math.atan(SENSOR_W / (2 * LENS_FOCAL)))
AFOV_VERTICAL = math.degrees(2 * math.atan(SENSOR_H / (2 * LENS_FOCAL)))

model = YOLO("yolov8n.pt")
results = model('test-image-3.jpeg', show=True)

image = cv2.imread('test-image-3.jpeg')

IMAGE_WIDTH, IMAGE_HEIGHT = image.shape[1], image.shape[0]
print('lens FOccal', LENS_FOCAL)
print('AFOV_h', AFOV_HORIZONTAL)
print('AFOV_v', AFOV_VERTICAL)


def calculate_distance(bottom_y_pos_of_object):
    print('bottom_pos', bottom_y_pos_of_object)
    x = bottom_y_pos_of_object - (IMAGE_HEIGHT / 2)  # odleglosc linii poziomej dolu obiektu wzgledem horyzontu
    y = IMAGE_HEIGHT / 2 - x  # odlegosci linii poziomej dolu obiektu wzglem dolu kadru

    """ 
    X/Y = ALPHA/BETHA
    then (X*BETA)/Y = ALPHA => BETA = ALPHA * (Y/X)
    SINCE ALPHA + BETHA = AFOV_H/2
    AFOV_H/2 = ALPHA * ( 1 + (Y/X) )
    ALPHA = (AFOV_H/2)/(1 + (Y/X)
    """

    alpha = (AFOV_VERTICAL / 2) / (1 + (y / x))

    return math.tan(math.radians(90 - alpha)) * CAMERA_POS_HEIGHT


def custom_boxes():
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x, y, x2, y2 = box.xyxy[0]
            x, y, x2, y2 = int(x), int(y), int(x2), int(y2)
            if y2 > 630:
                cv2.rectangle(image, (x, y), (x2, y2), (255, 255, 0), 3)
                print('Distance from this object aprx: ' + str(calculate_distance(y2)))

def draw_horizontal_line():
    pt1 = (0, 630)
    pt2 = (IMAGE_WIDTH, 630)
    cv2.line(image, pt1, pt2, (255, 255, 0), 3)

def drawLines():
    pass


# print('CALC DIST HORIZONT', calculate_distance((IMAGE_HEIGHT / 2)+1))
custom_boxes()
draw_horizontal_line()
# resized_image = cv2.resize(image, (int(IMAGE_WIDTH / 6), int(IMAGE_HEIGHT / 6)))
cv2.imshow('image +++', image)
cv2.waitKey(0)
