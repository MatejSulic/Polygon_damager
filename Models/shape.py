import numpy as np
from .point import Point

class Shape:
    def __init__(self, name: str, points: list[Point], contains_indices: list[int] = None):
        """
        Inicializace tvaru.

        :param name: Jméno tvaru.
        :param points: Seznam bodů, které tvoří tvar.
        :param contains_indices: Volitelný seznam indexů, které tyto body zabíraly
                                 v původním celém tvaru (klíčové pro re-kombinaci).
        """
        self.name = name
        self.points = points  # list[Point]
        
        # NOVÝ ATRIBUT: Ukládá indexy z původního, celého tvaru
        self.contains_indices = contains_indices if contains_indices is not None else [] 

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

        # 3. Vytvoříme NOVOU instanci Shape a zkopírujeme i indexy
        new_shape = Shape(name_to_use, new_points)
        
        # Klíčové: Zkopírujeme i seznam indexů
        new_shape.contains_indices = self.contains_indices.copy() 
        
        return new_shape