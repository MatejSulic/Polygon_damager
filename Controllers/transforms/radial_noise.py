import numpy as np

from Controllers.ShapeProcessor import get_centroid


def add_radial_noise(shape, centroid, alpha=0.05, lock_edges=True):
    """
    Každý bod se posune směrem od centroidu o náhodnou hodnotu [-max_damage, max_damage].
    lock_edges: první a poslední bod zůstávají na místě
    """
    new_shape = shape.copy( new_name=f"{shape.name}_radial_a{str(alpha)}")


    dx = np.array([p.x - centroid.x for p in new_shape.points])
    dy = np.array([p.y - centroid.y for p in new_shape.points])
    dist = np.sqrt(dx**2 + dy**2)
    # ochrana proti nulové vzdálenosti
    dist[dist==0] = 1.0

    # jednotkový směrový vektor
    ux = dx / dist
    uy = dy / dist

    # náhodný posun podél směru
    shift = np.random.uniform(-alpha, alpha, len(new_shape.points))
    if lock_edges:
        shift[0] = 0
        shift[-1] = 0

    for i, p in enumerate(new_shape.points):
        p.x += ux[i] * shift[i]
        p.y += uy[i] * shift[i]

    return new_shape
