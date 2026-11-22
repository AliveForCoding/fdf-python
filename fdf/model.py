from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    z: int
    color: str | None = None


class Map:
    def __init__(self, points: list[list[Point]]) -> None:
        self.points = points

    def __len__(self) -> int:
        return len(self.points)

    def __iter__(self) -> Iterator[list[Point]]:
        return iter(self.points)

    def neighbors(self, point: Point) -> list[Point]:
        result: list[Point] = []

        y = point.y
        x = point.x

        if y > 0:
            result.append(self.points[y - 1][x])

        if y < len(self.points) - 1:
            result.append(self.points[y + 1][x])

        if x > 0:
            result.append(self.points[y][x - 1])

        if x < len(self.points[y]) - 1:
            result.append(self.points[y][x + 1])

        return result