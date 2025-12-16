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

    
    

    # 2) generování tvarů s radiálním šumem
    num_shapes = 5  # počet tvarů k vygenerován
    is_area = True

    
    for area in [True, False]:

        for alpha in [0.03, 0.05, 0.07, 0.1]:
            for percentage in [0.2, 0.5]:


                GenerateRadialNoiseShapes(shape, alpha, percentage, num_shapes, area)
                GenerateRandomNoiseShapes(shape, alpha, percentage, num_shapes, area)
        


if __name__ == "__main__":
    main()