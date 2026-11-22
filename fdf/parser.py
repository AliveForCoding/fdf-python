from fdf.model import Point

class FdfError(Exception):
    pass


class MapFormatError(FdfError):
    pass

def parse_value(token: str, line: int, column: int) -> tuple[int, str | None]:
    parts = token.split(",")

    if len(parts) > 2:
        raise MapFormatError(
            f"строка {line}, колонка {column}: неправильный формат '{token}'"
        )

    try:
        z = int(parts[0])
    except ValueError:
        raise MapFormatError(
            f"строка {line}, колонка {column}: '{parts[0]}' — не целое число"
        )

    color = None

    if len(parts) == 2:
        color_text = parts[1]

        if not color_text.lower().startswith("0x"):
            raise MapFormatError(
                f"строка {line}, колонка {column}: неправильный цвет '{color_text}'"
            )

        hex_digits = color_text[2:]

        if not 1 <= len(hex_digits) <= 6:
            raise MapFormatError(
                f"строка {line}, колонка {column}: неправильный цвет '{color_text}'"
            )

        try:
            color_number = int(hex_digits, 16)
        except ValueError:
            raise MapFormatError(
                f"строка {line}, колонка {column}: неправильный цвет '{color_text}'"
            )

        color = f"#{color_number:06X}"
    return z, color

def parse_row(line_text: str, y: int, line_number: int) -> list[Point]:
    tokens = line_text.split()
    points: list[Point] = []

    for x, token in enumerate(tokens):
        z, color = parse_value(token, line_number, x + 1)

        point = Point(
            x=x,
            y=y,
            z=z,
            color=color,
        )

        points.append(point)

    return points
