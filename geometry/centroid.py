import numpy as np

from transforms.symmetry import mirror_x

def symmetric_x_centroid(shape):
    """
    Vrací (cx, cy) – těžiště shape.
    """
    other_half = mirror_x(shape)
    combined_points = shape.points + other_half.points

    x = [p.x for p in combined_points]
    y = [p.y for p in combined_points]
    cx = np.mean(x)
    cy = np.mean(y)
    return cx, cy
