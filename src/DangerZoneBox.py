class DangerZoneBox:

    def __init__(self, width_meters, height_meters):
        """
        :param width_meters:
        :param height_meters:
        """
        self.width_meters = width_meters
        self.height_meters = height_meters
        self.top_left = 0
        self.top_right = 0
        self.bottom_left = 0
        self.bottom_right = 0
        self.left_line_slope = 0
        self.left_line_y_intercept = 0
        self.left_line_y_intercept = 0  # y = ax+b      <- its b
        self.right_line_slope = 0
        self.right_line_y_intercept = 0
        self.top_line_y = 0

    def set_zone_borders(self, top_left, top_right, bottom_left, bottom_right):
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

        # setting y of top point as a formula of top (back) of the danger zone since y = ax+b => y = 0*x + b => y = b
        self.top_line_y = top_left[1]

        # setting side line formulas params
        self.left_line_slope, self.left_line_y_intercept = self.calculate_line(top_left, bottom_left)
        self.right_line_slope, self.right_line_y_intercept = self.calculate_line(top_right, bottom_right)

    def get_zone_borders(self):
        return self.top_left, self.top_right, self.bottom_left, self.bottom_right

    def calculate_line(self, top, bottom):
        """
        Top & bottom are tuples (int, int)
        :param top:
        :param bottom:
        :return:
        """
        x1, y1 = bottom
        x2, y2 = top
        a = (y2 - y1) / (x2 - x1)

        # Calculate y-intercept using one of the points
        b = y1 - a * x1

        return a, b

    def is_point_inside(self, x, y):
        # y = ax + b
        # then x = (y-b) / a
        # to check if point (x1, y2) is between the lines horizontally we check if
        #

        left_line_check = self.left_line_slope * x + self.left_line_y_intercept
        right_line_check = self.right_line_slope * x + self.right_line_y_intercept

        if (y < left_line_check and y < right_line_check) or y < self.top_line_y:
            return False
        else:
            return True

    def is_object_inside(self, box):
        x, y, x2, y2 = box.xyxy[0]
        x, y, x2, y2 = int(x), int(y), int(x2), int(y2)
        return self.is_point_inside(x, y) or self.is_point_inside(x2, y2) or self.is_point_inside(x2, y) or self.is_point_inside(x, y2)

