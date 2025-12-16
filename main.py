from Controllers.ShapeDrawer import Drawer
from Controllers.ShapeProcessor import get_centroid,mirror_y,shape_connect
from Controllers.FileLoader.FileLoader import load_geometry
from Controllers.Shape_Generator import GenerateRadialNoiseShapes, GenerateRandomNoiseShapes
from Controllers.transforms.radial_noise import add_radial_noise
import matplotlib.pyplot as plt

def main():
    # 1) načtení tvarů ze souboru
    shapes = load_geometry("./Controllers/FileLoader/shapes_clean.txt")
    shape = shapes[list(shapes.keys())[0]]

    # 2) generování tvarů s radiálním šumem
    num_shapes = 5  # počet tvarů k vygenerován
    alpha = 0.2  # maximální posun bodu
    GenerateRadialNoiseShapes(shape, alpha, num_shapes)

    GenerateRandomNoiseShapes(shape, alpha, num_shapes)
    


if __name__ == "__main__":
    main()