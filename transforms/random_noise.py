import numpy as np

def add_random_noise(shape, alpha=0.05, lock_edges=True):
    """
    alpha = maximální posun v ose x a y -> náhodně v rozsahu [-alpha, +alpha]
    """
    new = shape.clone(shape.name + "_noisy")

    dx = np.random.uniform(-alpha, alpha, len(shape.points))
    dy = np.random.uniform(-alpha, alpha, len(shape.points))

    if lock_edges:
        dx[0] = dy[0] = 0
        dx[-1] = dy[-1] = 0

    for i, p in enumerate(new.points):
        p.x += dx[i]
        p.y += dy[i]

    return new
