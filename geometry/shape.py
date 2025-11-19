import numpy as np
from .point import Point

class Shape:
    def __init__(self, name, points):
        self.name = name
        self.points = points  # list[Point]

    @property
    def x(self):
        return np.array([p.x for p in self.points])

    @property
    def y(self):
        return np.array([p.y for p in self.points])

    def clone(self, new_name=None):
        """Vrací hlubokou kopii shape."""
        return Shape(
            new_name or self.name,
            [Point(p.x, p.y) for p in self.points]
        )

    def pipe(self, func):
        """Umožňuje elegantní řetězení transformací."""
        return func(self)
