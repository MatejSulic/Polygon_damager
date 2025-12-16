import matplotlib.pyplot as plt
from Controllers.ShapeDrawer import Drawer
from Controllers.ShapeProcessor import get_centroid, mirror_y, shape_connect
from Controllers.FileLoader.FileLoader import load_geometry
from Controllers.transforms.radial_noise import add_radial_noise
from Controllers.transforms.random_noise import add_random_noise
from Models.shape import Shape


def GenerateRadialNoiseShapes(shape: Shape, alpha: float, num_shapes: int):

    other_half = mirror_y(shape)
                
    shape_before_transform = shape_connect(shape, other_half)
                
    centroid = get_centroid(shape_before_transform)

    for i in range(num_shapes):
        
            
            
            result = add_radial_noise(other_half, centroid, alpha)

            shape_to_save = shape_connect(shape, result)


            # Vykreslení výsledku
            d = Drawer()
            d.draw_shape(shape, color="blue", linewidth=2)  # původní tvar
            d.draw_shape(result, color="black", linewidth=2)     # deformovaný
            d.set_title(f"Radial Noise α={alpha} Id={i}")  # Nastavení titulku

            shape_name = shape_to_save.name+"_"+str(i)+".png"
            d.save(shape_name, output_dir="radial_noise_results")
            
        
            plt.close(d.fig) 
    print(f"Úspěšně vygenerováno a uloženo {num_shapes} obrázků do složky 'radial_noise_results'.")

def GenerateRandomNoiseShapes(shape: Shape, alpha: float, num_shapes: int):

    other_half = mirror_y(shape)    

    for i in range(num_shapes):
        
    
            result = add_random_noise(other_half, alpha)

            shape_to_save = shape_connect(shape, result)


            # Vykreslení výsledku
            d = Drawer()
            d.draw_shape(shape, color="blue", linewidth=2)  # původní tvar
            d.draw_shape(result, color="black", linewidth=2)     # deformovaný

            d.set_title(f"Random Noise α={alpha} Id={i}")  # Nastavení titulku
            shape_name = shape_to_save.name+"_"+str(i)+".png"
            d.save(shape_name, output_dir="random_noise_results")
            
        
            plt.close(d.fig) 
    print(f"Úspěšně vygenerováno a uloženo {num_shapes} obrázků do složky 'random_noise_results'.")