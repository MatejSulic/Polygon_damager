from Controllers.ShapeDrawer import Drawer
from Controllers.ShapeProcessor import get_centroid,mirror_y,shape_connect, shape_connect_by_index, split_shape_by_percentage
from Controllers.FileLoader.FileLoader import load_geometry
from Controllers.Shape_Generator import GenerateRadialNoiseShapes, GenerateRandomNoiseShapes
from Controllers.transforms.radial_noise import add_radial_noise
import matplotlib.pyplot as plt

from Controllers.transforms.random_noise import add_random_noise

def main():
    # 1) načtení tvarů ze souboru
    shapes = load_geometry("./Controllers/FileLoader/shapes_clean.txt")
    shape = shapes[list(shapes.keys())[0]]


    shape_side = mirror_y(shape)   # vytvoření zrcadleného tvaru pro demonstraci


    shape_movable, shape_fixed = split_shape_by_percentage(shape_side, 0.5)

    shape_movebale_deformation = add_random_noise(shape_movable, alpha=0.2, lock_edges=False)



    shape_side = shape_connect_by_index(shape_movebale_deformation, shape_fixed, len(shape_side.points), shape_side.name)

  
    drawer = Drawer()
    drawer.draw_points(shape_movebale_deformation, color="red", size=10)
    drawer.draw_shape(shape, color="black", linewidth=1)
    drawer.draw_shape(shape_side, color="blue", linewidth=1)
    drawer.set_title("Tvar s radiálním šumem na polovině bodů")
    drawer.show()





    # # 2) generování tvarů s radiálním šumem
    # num_shapes = 5  # počet tvarů k vygenerován
    # alpha = 0.2  # maximální posun bodu
    # GenerateRadialNoiseShapes(shape, alpha, num_shapes)

    # GenerateRandomNoiseShapes(shape, alpha, num_shapes)
    


if __name__ == "__main__":
    main()