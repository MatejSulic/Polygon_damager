import numpy as np
from geometry.shape import Shape

def select_random_points(shape: Shape, ratio: float = 0.25, seed=None):
    if seed is not None:
        np.random.seed(seed)
    n_points = len(shape.points)
    n_select = int(n_points * ratio)
    indices = np.random.choice(range(n_points), n_select, replace=False).tolist()
    subset_points = [shape.points[i] for i in indices]
    subset_shape = Shape(shape.name + f"_subset_{int(ratio*100)}", subset_points)
    return subset_shape, indices

def merge_shapes(original: Shape, modified: Shape, modified_indices):
    """
    Vrátí nový Shape, kde body na indexech modified_indices jsou z modified,
    ostatní zůstávají z original.
    """
    if len(modified.points) != len(modified_indices):
        raise ValueError("Počet bodů v modified_shape a modified_indices se musí shodovat")

    all_points = []
    for i in range(len(original.points)):
        if i in modified_indices:
            idx = modified_indices.index(i)
            all_points.append(modified.points[idx])
        else:
            all_points.append(original.points[i])
    return Shape(original.name + "_merged", all_points)
