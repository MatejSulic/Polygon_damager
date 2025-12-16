class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


    def copy(self):
        """Vytvoří novou instanci Point se stejnými souřadnicemi."""
        return Point(self.x, self.y)