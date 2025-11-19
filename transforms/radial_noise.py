import numpy as np
from geometry.centroid import symmetric_x_centroid
from geometry.shape import Shape
from geometry.point import Point

def add_radial_noise(shape, max_damage=0.05, lock_edges=True):
    """
    Každý bod se posune směrem od centroidu o náhodnou hodnotu [-max_damage, max_damage].
    lock_edges: první a poslední bod zůstávají na místě
    """
    new_shape = shape.clone(shape.name + "_radial")

    cx, cy = symmetric_x_centroid(new_shape)

    dx = np.array([p.x - cx for p in new_shape.points])
    dy = np.array([p.y - cy for p in new_shape.points])
    dist = np.sqrt(dx**2 + dy**2)
    # ochrana proti nulové vzdálenosti
    dist[dist==0] = 1.0

    # jednotkový směrový vektor
    ux = dx / dist
    uy = dy / dist

    # náhodný posun podél směru
    shift = np.random.uniform(-max_damage, max_damage, len(new_shape.points))
    if lock_edges:
        shift[0] = 0
        shift[-1] = 0

    for i, p in enumerate(new_shape.points):
        p.x += ux[i] * shift[i]
        p.y += uy[i] * shift[i]

    return new_shape
