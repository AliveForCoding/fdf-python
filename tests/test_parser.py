import pytest

from fdf.parser import MapFormatError, parse_map


def test_parse_map_size() -> None:
    map_data = parse_map("0 1 2\n3 4 5\n6 7 8\n")

    assert len(map_data) == 3
    assert len(map_data.points[0]) == 3


def test_parse_point_values() -> None:
    map_data = parse_map("0 1 2\n3 -2 5\n6 7 8\n")

    point = map_data.points[1][1]

    assert point.x == 1
    assert point.y == 1
    assert point.z == -2


def test_point_neighbors() -> None:
    map_data = parse_map("0 1 2\n3 4 5\n6 7 8\n")
    point = map_data.points[1][1]

    neighbors = map_data.neighbors(point)

    assert len(neighbors) == 4
    assert {neighbor.z for neighbor in neighbors} == {1, 3, 5, 7}


def test_point_coordinates() -> None:
    map_data = parse_map("10 20 30\n40 50 60\n")
    point = map_data.points[1][2]

    assert point.x == 2
    assert point.y == 1
    assert point.z == 60


def test_parse_color() -> None:
    map_data = parse_map("0,0xFF0000 1 2\n")
    point = map_data.points[0][0]

    assert point.z == 0
    assert point.color == "#FF0000"


def test_negative_height() -> None:
    map_data = parse_map("-5 -1 0\n")

    assert map_data.points[0][0].z == -5
    assert map_data.points[0][1].z == -1


def test_uneven_map_raises_error() -> None:
    with pytest.raises(MapFormatError):
        parse_map("0 1 2\n3 4\n")

def test_empty_map_raises_error() -> None:
    with pytest.raises(MapFormatError):
        parse_map("")