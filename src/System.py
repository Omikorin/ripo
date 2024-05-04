from Camera import Camera
import math
import cv2
from ultralytics import YOLO


class System:
    def __init__(self):
        self.results = None
        self.image_width = None
        self.image_height = None
        self.image = None
        self.camera = None
        self.box_height = None
        self.box_width = None
        self.camera_position_height = None
        self.focal_length = None
        self.sensor_height = None
        self.sensor_width = None

    def configure(self, sensor_width, sensor_height, focal_length, camera_position_height, box_height,
                  box_width):
        self.sensor_width = sensor_width
        self.sensor_height = sensor_height
        self.focal_length = focal_length
        self.camera_position_height = camera_position_height
        self.box_height = box_height
        self.box_width = box_width

        self.create_camera()

    def create_camera(self):
        self.camera = Camera(self.sensor_width, self.sensor_height, self.focal_length, self.camera_position_height)

    def load_image(self, image):
        self.image = image
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]

    def analyse_image(self):
        model = YOLO("yolov8n.pt")
        self.results = model('test-apsc.jpg', show=True)

    # UTILITY FUNCTIONS
    def calculate_distance(self, bottom_y_pos_of_object):
        # print('bottom_pos', bottom_y_pos_of_object)

        x = bottom_y_pos_of_object - (self.image_height / 2)  # odleglosc linii poziomej dolu obiektu wzgledem horyzontu
        y = self.image_height / 2 - x  # odlegosci linii poziomej dolu obiektu wzglem dolu kadru

        """ 
        X/Y = ALPHA/BETHA
        then (X*BETA)/Y = ALPHA => BETA = ALPHA * (Y/X)
        SINCE ALPHA + BETHA = AFOV_H/2
        AFOV_H/2 = ALPHA * ( 1 + (Y/X) )
        ALPHA = (AFOV_H/2)/(1 + (Y/X)
        """

        alpha = (self.camera.afov_vertical / 2) / (1 + (y / x))

        return math.tan(math.radians(90 - alpha)) * self.camera.camera_position_height

    def calc_y_pos_from_distance(self, distance_y):
        """
        since we have distance = L
        height = H
        we can calculate BETA+GAMMA
        Then ALPHA = 90 - BETA - GAMMA
        BETA = VERTICAL_AFOV/2 - ALPHA
        """

        l = distance_y
        h = self.camera.camera_position_height
        v_afov = self.camera.afov_vertical
        beta_plus_gamma = math.degrees(math.atan(l / h))
        alpha = 90 - beta_plus_gamma
        beta = v_afov / 2 - alpha

        """
        now since X/Y = ALPHA/BETHA
        and X + Y = IMAGE_HEIGHT/2

        X = (ALPHA/BETA) * Y
        Y = IMAGE_HEIGHT / 2 - X

        then

        X = (ALPHA/BETA) * (IMAGE_HEIGHT / 2 - X)
        (1 + (ALPHA/BETA)) * X = (IMAGE_HEIGHT / 2) * (ALPHA/BETA)
        X = [(IMAGE_HEIGHT / 2) * (ALPHA/BETA)] / [(1 + (ALPHA/BETA))]
        """

        x = ((self.image_height / 2) * (alpha / beta)) / (1 + (alpha / beta))
        y = (self.image_height / 2) - x

        # where x is dist from middle (horizon)
        # and y is dist from bottom of image
        # therefore line will be at IMAGE_HEIGHT/2 + x

        return x, y

    def calc_box(self, distance_x, distance_y):
        """
        let distance_x be the base of isosceles triangle with top angle equal to AFOV_HORIZONTAL
        and height of h

        therefore half of this triangle has base of a = distance/2
        angle alpha = AFOV_HORIZONTAL / 2
        and height b = h
        we look for b

        tg alpha = a / b => b = a / tg alpha
        """

        a = distance_x / 2
        alpha = self.camera.afov_horizontal / 2
        print('alpha', alpha)
        b = a / math.tan(math.radians(alpha))
        print('b:', b)

        """
        having H we can calculate its position on image using calc_y_pos_from_distance(H)
        which gives x - dist from horizon (equal IMAGE_HEIGHT / 2), and y being IMAGE_HEIGHT / 2 - x

        Possible cases:
        - x < IMAGE_HEIGHT / 2   -   probably not gonna happen (??) it means that camera has very narrow view than
                                     and lines bottom points will be on screen
        - x > IMAGE_HEIGHT / 2   -   means that bottom points will be out of the screen. In some cases this lines might
                                     not appear at all
        """

        x, y = self.calc_y_pos_from_distance(b)
        print('picture pos for 12 is: ', x, ' from middle, wehere IMG_HEIGHT/2 = ', self.image_height / 2)

        """
        assuming that image is not limited by height we will calculate position of bottom points as 
        x_axis = IMAGE_HEIGHT / 2 + x
        and 
        y_axis = 0 for left and y_axis = IMAGE_WIDTH for right
        """

        bottom_left = (0, self.image_height / 2 + x)
        bottom_right = (self.image_width, self.image_height / 2 + x)
        """
        now we want to calc end of box (top). 
        W know its H meters away so its x_axis position will be calc_y_pos_from_distance(H)
        top_left y_axis will be:
        let k be distance on image from top of box to horizon (IMAGE_HEIGHT / 2)
        let l be x (distance to place where image could be wide enough)
        also
        let m be width of box on bottom (which will always be IMAGE_WIDTH ???)
        let n be width of box on top which we look for

        knowing that l/k = m/n 
        we can calculate n as m * k / l
        """
        H = distance_y
        k = self.calc_y_pos_from_distance(H)[0]
        l = x
        m = self.image_width
        n = m * (k / l)
        print(f"k = {k}, l = {l}, m = {m}, n = {n}")

        """
        knowing n we can calculate 
        top_left x_axis  = IMAGE_WIDTH / 2 - n / 2
        top_right x_axis  = IMAGE_HEIGHT / 2 + n / 2 
        """

        top_left = (self.image_width / 2 - n / 2, self.image_height / 2 + k)
        top_right = (self.image_width / 2 + n / 2, self.image_height / 2 + k)

        # CHANGING TO INTEGER!
        top_left = tuple(map(int, top_left))
        top_right = tuple(map(int, top_right))
        bottom_left = tuple(map(int, bottom_left))
        bottom_right = tuple(map(int, bottom_right))

        print('bottom_left', bottom_left)
        print('bottom_right', bottom_right)
        print('top_left', top_left)
        print('top_right', top_right)

        return top_left, top_right, bottom_left, bottom_right

    def draw_line_at(self, distance):
        x, y = self.calc_y_pos_from_distance(distance)
        print('x: ', x)

        line_y = math.floor((self.image_height / 2) + x)

        pt1 = (0, line_y)
        pt2 = (self.image_width, line_y)
        cv2.line(self.image, pt1, pt2, (0, 255, 255), 3)

    def draw_test_lines(self):
        self.draw_line_at(1.5)
        self.draw_line_at(3.0)
        self.draw_line_at(4.5)
        self.draw_line_at(6.0)
        self.draw_line_at(7.5)

    def draw_box(self, box_width, box_height):
        # we need for points
        # top_left, top_right
        # bottom_left, bottom_right

        top_left, top_right, bottom_left, bottom_right = self.calc_box(box_width, box_height)

        cv2.line(self.image, top_left, bottom_left, (0, 255, 255), 3)
        cv2.line(self.image, top_right, bottom_right, (0, 255, 255), 3)

    def custom_boxes(self):
        for r in self.results:
            boxes = r.boxes
            for box in boxes:
                x, y, x2, y2 = box.xyxy[0]
                x, y, x2, y2 = int(x), int(y), int(x2), int(y2)
                if y2 > 630:
                    cv2.rectangle(self.image, (x, y), (x2, y2), (255, 255, 0), 3)
                    print('Distance from this object aprx: ' + str(self.calculate_distance(y2)))

    def run_test(self):
        self.analyse_image()
        self.custom_boxes()
        # cv2.imshow('Raw img from model', self.image)
        # perform overlay and drawing
        self.draw_test_lines()
        self.draw_box(self.box_width, self.box_height)
        cv2.imshow('Img after drawing', self.image)
        cv2.waitKey(0)