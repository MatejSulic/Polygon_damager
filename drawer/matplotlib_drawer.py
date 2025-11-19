import matplotlib.pyplot as plt

class Drawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(9, 7))
        self.ax.set_aspect("equal")
        self.ax.grid(True, alpha=0.3)

    def draw_shape(self, shape, color="black", linewidth=2):
        self.ax.plot(shape.x, shape.y, color=color, linewidth=linewidth)

    def draw_points(self, shape, color="red", size=5):
        self.ax.scatter(shape.x, shape.y, s=size, color=color)

    def show(self):
        plt.show()
