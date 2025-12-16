from pathlib import Path
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

    def set_title(self, title):
        """Nastaví titulek (název) grafu."""
        self.ax.set_title(title)

    def show(self):
        plt.show()

    def save(self, filename, output_dir=""):
       
        base_dir = "output_figures"
        
        # 1. Složení cesty
        if output_dir:
            # Příklad: base_dir="output_figures", output_dir="modely_a"
            # -> full_dir_path = "output_figures/modely_a"
            full_dir_path = Path(base_dir) / output_dir
        else:
            # Příklad: base_dir="output_figures", output_dir=""
            # -> full_dir_path = "output_figures"
            full_dir_path = Path(base_dir)
            
        # 2. Vytvoření složky, pokud neexistuje
        # (parents=True vytvoří i nadřazené, exist_ok=True zabrání chybě, pokud složka existuje)
        full_dir_path.mkdir(parents=True, exist_ok=True)
        
        # 3. Spojení cesty ke složce s názvem souboru
        full_path = full_dir_path / filename
        
        # 4. Uložení obrázku
        self.fig.savefig(full_path)