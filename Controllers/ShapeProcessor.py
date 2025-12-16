import numpy as np

from Models.point import Point


def shape_connect(shape1, shape2):
    new_name = f"{shape1.name}_plus_{shape2.name}"
    shape = shape1.copy( new_name=new_name)
    shape.points.extend([p.copy() for p in shape2.points])
    return shape


def get_centroid(shape):
    """
    Vrací (cx, cy) – těžiště shape.
    """
    x = [p.x for p in shape.points]
    y = [p.y for p in shape.points]
    cx = np.mean(x)
    cy = np.mean(y)
    return Point(cx, cy)


def mirror_y(shape):

    """Vrátí shape zrcadlený přes osu Y (x → -x)."""
    mirrored_shape = shape.copy(new_name=f"{shape.name}_mirrored_y")

    for p in mirrored_shape.points:
        p.x = -p.x

    return mirrored_shape

def mirror_x(shape):

    """Vrátí shape zrcadlený přes osu X (y → -y)."""

    mirrored_shape = shape.copy(new_name=f"{shape.name}_mirrored_x")

    for p in mirrored_shape.points:
        p.y = -p.y

    return mirrored_shape

