import sys

from fdf.interface import App
from fdf.parser import load_map


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.fdf>", file=sys.stderr)
        return 2

    try:
        map_data = load_map(sys.argv[1])
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    app = App(map_data)
    app.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())