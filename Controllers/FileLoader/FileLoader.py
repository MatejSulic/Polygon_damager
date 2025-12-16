from Models.point import Point
from Models.shape import Shape

def load_geometry(filepath):
    shapes = {}
    current_name = None
    curr_points = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            if not line: 
                continue

            if line.startswith("#"):
                if current_name:
                    shapes[current_name] = Shape(current_name, curr_points)

                current_name = line.lstrip("# ").strip()
                curr_points = []
                continue

            try:
                x, y = map(float, line.split())
                curr_points.append(Point(x, y))
            except:
                pass

    if current_name:
        shapes[current_name] = Shape(current_name, curr_points)

    return shapes
