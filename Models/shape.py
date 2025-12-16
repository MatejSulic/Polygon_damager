import numpy as np
from .point import Point

class Shape:
    def __init__(self,name: str, points: list[Point]):
        self.name = name
        self.points = points  # list[Point]

    @property
    def x(self):
        return np.array([p.x for p in self.points])

    @property
    def y(self):
        return np.array([p.y for p in self.points])

 
    def copy(self, new_name=None):
        """
        Vytvoří nezávislou kopii objektu Shape.
        Jméno 'name' se zkopíruje, body se HLUBOČE zkopírují.
        """
        # 1. Zkopírujeme body HLUBOČE
        new_points = [p.copy() for p in self.points]

        # 2. Určíme nové jméno
        name_to_use = new_name if new_name is not None else self.name + "_copy"

        # 3. Vytvoříme a vrátíme NOVOU instanci Shape
        return Shape(name_to_use, new_points)
  

