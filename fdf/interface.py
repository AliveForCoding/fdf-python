import tkinter as tk

from fdf.model import Map, Point
from fdf.projection import Camera


class App:
    def __init__(self, map_data: Map | None) -> None:
        self.map_data = map_data
        self.camera = Camera()

        self.root = tk.Tk()
        self.root.title("Fdf - Wireframe Map")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(
            self.root,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.on_resize)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

    def get_edge_color(self, point1: Point, point2: Point) -> str:
        if point1.color is None:
            if point2.color is None:
                return "#DDE7F0"
            return point2.color

        if point2.color is None:
            return point1.color

        if point1.z >= point2.z:
            return point1.color

        return point2.color


    def on_resize(self, event: tk.Event) -> None:
        if self.map_data is None:
            return

        self.camera.fit(
            self.map_data,
            event.width,
            event.height,
        )
        self.draw()

    def draw(self) -> None:
        self.canvas.delete("all")

        if self.map_data is None:
            return

        screen_points: list[list[tuple[float, float]]] = []

        for map_row in self.map_data:
            screen_row: list[tuple[float, float]] = []

            for map_point in map_row:
                screen_x, screen_y = self.camera.transform(map_point)
                screen_row.append((screen_x, screen_y))

            screen_points.append(screen_row)

        for y, screen_row in enumerate(screen_points):
            for x, screen_point in enumerate(screen_row):
                current_point = self.map_data.points[y][x]

                if x < len(screen_row) - 1:
                    right_point = screen_row[x + 1]
                    right_map_point = self.map_data.points[y][x + 1]

                    self.canvas.create_line(
                        screen_point[0],
                        screen_point[1],
                        right_point[0],
                        right_point[1],
                        fill=self.get_edge_color(
                            current_point,
                            right_map_point,
                        ),
                    )

                if y < len(screen_points) - 1:
                    lower_point = screen_points[y + 1][x]
                    lower_map_point = self.map_data.points[y + 1][x]

                    self.canvas.create_line(
                        screen_point[0],
                        screen_point[1],
                        lower_point[0],
                        lower_point[1],
                        fill=self.get_edge_color(
                            current_point,
                            lower_map_point,
                        ),
                    )

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = App(None)
    app.run()