import matplotlib.pyplot as plt
from Controllers.ShapeDrawer import Drawer
from Controllers.ShapeProcessor import get_centroid, mirror_y, shape_connect, shape_connect_by_index, split_shape_by_percentage
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



def GenerateRandomNoiseShapes(shape: Shape, alpha: float, percentage: float, num_shapes: int):
    alpha_str = str(alpha).replace('.', '_') # 0.1 -> 0_1
    pct_str = int(percentage * 100)           # 0.2 -> 20
    
    output_dir = f"random_noise_per{pct_str}_a{alpha_str}"

    # Čistá, neměnná šablona poloviny (pro opakované použití)
    other_half_template = mirror_y(shape) 

    print(f"Generuji tvary z šablony: {other_half_template.name}") 
    
    # 1. Tuto deformující funkci si musíme připravit jako callable
    # Použijeme lambda funkci pro fixaci alpha a vypnutí lock_edges (pokud jej add_random_noise stále má)
    # Předpokládáme, že add_random_noise má parametr lock_edges=False, protože to řeší split_shape.
    noise_callable = lambda s: add_random_noise(s, alpha=alpha, lock_edges=False) 


    for i in range(num_shapes):
        
        # 1. Pokaždé začneme s ČERSTVOU kopií šablony k deformaci
        half_to_deform = other_half_template.copy(new_name=None)
        
        # 2. Rozdělíme čerstvou kopii
        # V každé iteraci se náhodný výběr indexů opakuje.
        shape_movable, shape_fixed = split_shape_by_percentage(half_to_deform, percentage)  

        deformed_movable = noise_callable(shape_movable)


        # 4. Spojení (Combine)
        # Použijeme deformovanou část a pevnou část z této iterace.
        result = shape_connect_by_index(
            deformed_movable, 
            shape_fixed, 
            len(half_to_deform.points), 
            deformed_movable.name
        )

        shape_to_save = shape_connect(shape, result) # Spojení čisté poloviny s deformovanou


        # Vykreslení výsledku
        d = Drawer()
        # Vykreslujeme body z aktuální iterace
        d.draw_points(deformed_movable, color="red", size=10)
        d.draw_points(shape_fixed, color="green", size=10)
        d.draw_shape(shape, color="blue", linewidth=2)
        d.draw_shape(result, color="black", linewidth=2)

        d.set_title(f"Random Noise α={alpha} Deformace: {len(shape_movable.points)}/{len(half_to_deform.points)-2} Id={i} ")

        shape_name = shape_to_save.name+"_"+str(i)+".png"

        d.save(shape_name, output_dir)
        
        plt.close(d.fig)

    print(f"Úspěšně vygenerováno a uloženo {num_shapes} obrázků do složky {output_dir}.")

