def _is_left(p0, p1, p2):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


class DangerZoneBox:

    def __init__(self, width_meters, height_meters):
        """
        :param width_meters:
        :param height_meters:
        """
        self.width_meters = width_meters
        self.height_meters = height_meters
        self.top_left = (0, 0)
        self.top_right = (0, 0)
        self.bottom_left = (0, 0)
        self.bottom_right = (0, 0)
        self.left_line_slope = 0
        self.left_line_y_intercept = 0
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

    def calculate_line(self, point1, point2):
        """
        Calculate the slope and y-intercept of the line passing through two points.
        """
        x1, y1 = point1
        x2, y2 = point2
        a = (y2 - y1) / (x2 - x1)  # slope

        # Calculate y-intercept using one of the points
        b = y1 - a * x1

        return a, b

    def is_point_inside(self, point):
        vertices = [self.top_left, self.top_right, self.bottom_right, self.bottom_left]
        winding_number = 0

        for i in range(len(vertices)):
            if vertices[i][1] <= point[1]:
                if vertices[(i + 1) % len(vertices)][1] > point[1]:
                    if _is_left(vertices[i], vertices[(i + 1) % len(vertices)], point) > 0:
                        winding_number += 1
            else:
                if vertices[(i + 1) % len(vertices)][1] <= point[1]:
                    if _is_left(vertices[i], vertices[(i + 1) % len(vertices)], point) < 0:
                        winding_number -= 1

        return winding_number != 0

    def is_object_inside(self, box):
        """
        Check if any corner of the object's bounding box is inside the danger zone.
        """
        x1, y1, x2, y2 = box.xyxy[0]
        corners = [(x1, y1), (x2, y2), (x1, y2), (x2, y1)]

        return any(self.is_point_inside((x, y)) for x, y in corners)
