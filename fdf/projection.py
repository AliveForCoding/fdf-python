import math

from fdf.model import Map, Point


def project_point(point: Point, z_scale: float = 1.0) -> tuple[float, float]:
    angle = math.radians(30)

    x_projected = (point.x - point.y) * math.cos(angle)
    y_projected = (point.x + point.y) * math.sin(angle) - point.z * z_scale

    return x_projected, y_projected

class Camera:
    def __init__(self) -> None:
        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.z_scale = 1.0

    def transform(self, point: Point) -> tuple[float, float]:
        x_projected, y_projected = project_point(point, self.z_scale)

        x = x_projected * self.scale + self.offset_x
        y = y_projected * self.scale + self.offset_y

        return x, y

    
    def fit(self, map_data: Map, width: int, height: int) -> None:
        projected_points = [
            project_point(point, self.z_scale)
            for row in map_data
            for point in row
        ]

        min_x = min(x for x, y in projected_points)
        max_x = max(x for x, y in projected_points)
        min_y = min(y for x, y in projected_points)
        max_y = max(y for x, y in projected_points)

        map_width = max_x - min_x
        map_height = max_y - min_y

        if map_width == 0 or map_height == 0:
            self.scale = 1.0
        else:
            scale_x = width / map_width
            scale_y = height / map_height
            self.scale = min(scale_x, scale_y) * 0.9

        self.offset_x = (width - map_width * self.scale) / 2 - min_x * self.scale
        self.offset_y = (height - map_height * self.scale) / 2 - min_y * self.scale