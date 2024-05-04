import math


class Camera:
    def __init__(self, sensor_width, sensor_height, focal_length, camera_position_height, afov_deg  ):
        self.sensor_width = sensor_width
        self.sensor_height = sensor_height
        self.focal_length = focal_length
        self.camera_position_height = camera_position_height
        self.afov_deg = afov_deg

        self.calculate_afov_horizontal_and_vertical()

        self.calculate_focal_length()   # will overwrite the given focal length


    def calculate_focal_length(self):

        # Convert AFOV from degrees to radians
        afov_rad = math.radians(self.afov_deg)

        # Calculate focal length
        focal_length = (self.sensor_width / 2) / math.tan(afov_rad / 2)

        # Adjust focal length based on sensor aspect ratio
        focal_length *= (self.sensor_height / self.sensor_width)

        self.focal_length = focal_length

        return focal_length

    def calculate_afov_horizontal_and_vertical(self):
        self.afov_horizontal = math.degrees(2 * math.atan(self.sensor_width / (2 * self.focal_length)))
        self.afov_vertical = math.degrees(2 * math.atan(self.sensor_height / (2 * self.focal_length)))

