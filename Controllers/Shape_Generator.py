import matplotlib.pyplot as plt
from Controllers.ShapeDrawer import Drawer
from Controllers.ShapeProcessor import get_centroid, mirror_y, shape_connect, shape_connect_by_index, split_shape_by_percentage
from Controllers.FileLoader.FileLoader import load_geometry
from Controllers.transforms.radial_noise import add_radial_noise
from Controllers.transforms.random_noise import add_random_noise
from Models.shape import Shape

# Ponechávám GenerateRandomNoiseShapes beze změny, jelikož je správná.

def GenerateRadialNoiseShapes(shape: Shape, alpha: float, percentage: float, num_shapes: int):
    
    # 1. NASTAVENÍ SLOŽKY
    alpha_str = str(alpha).replace('.', '_') # 0.1 -> 0_1
    pct_str = int(percentage * 100)           # 0.2 -> 20
    
    output_dir = f"radial_noise_per{pct_str}_a{alpha_str}"

    # Čistá, neměnná šablona poloviny (pro opakované použití)
    other_half_template = mirror_y(shape) 
                
    shape_before_transform = shape_connect(shape, other_half_template)
    # Centroid musí být počítán Z CELÉHO, nesymetrického tvaru pro správný směr šumu
    centroid = get_centroid(shape_before_transform)

    print(f"Generuji tvary z šablony: {other_half_template.name}") 
    
    # 2. PŘÍPRAVA DEFORMAČNÍHO CALLABLE
    # Tato lambda funkce fixuje centroid a alpha, a přijímá Shape
    radial_noise_callable = lambda s: add_radial_noise(s, centroid, alpha, lock_edges=False) 


    for i in range(num_shapes):
        
        # 1. Pokaždé začneme s ČERSTVOU kopií šablony k deformaci
        half_to_deform = other_half_template.copy(new_name=None)
        
        # 2. Rozdělíme čerstvou kopii (Split)
        # V každé iteraci se náhodný výběr indexů opakuje.
        shape_movable, shape_fixed = split_shape_by_percentage(half_to_deform, percentage)  

        # 3. Deformace (pouze jednou pro tuto iteraci)
        deformed_movable = radial_noise_callable(shape_movable)


        # 4. Spojení (Combine)
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
        d.draw_points(deformed_movable, color="red", size=10) # Pohyblivá (deformovaná) sada
        d.draw_points(shape_fixed, color="green", size=10)    # Pevná sada
        d.draw_shape(shape, color="blue", linewidth=2)
        d.draw_shape(result, color="black", linewidth=2)

        # Ujistíme se, že ve výpisu je i info o procentuální deformaci
        d.set_title(f"Radial Noise α={alpha} Deformace: {len(shape_movable.points)}/{len(half_to_deform.points)-2} Id={i} ")

        shape_name = shape_to_save.name+f"_{i}.png"

        d.save(shape_name, output_dir)
        
        plt.close(d.fig)

    print(f"Úspěšně vygenerováno a uloženo {num_shapes} obrázků do složky {output_dir}.")


def GenerateRandomNoiseShapes(shape: Shape, alpha: float, percentage: float, num_shapes: int):
    # ... (Stávající kód GenerateRandomNoiseShapes je nyní správný, ponechávám jej beze změny) ...
    alpha_str = str(alpha).replace('.', '_') 
    pct_str = int(percentage * 100)           
    
    output_dir = f"random_noise_per{pct_str}_a{alpha_str}"

    other_half_template = mirror_y(shape) 

    print(f"Generuji tvary z šablony: {other_half_template.name}") 
    
    noise_callable = lambda s: add_random_noise(s, alpha=alpha, lock_edges=False) 


    for i in range(num_shapes):
        
        half_to_deform = other_half_template.copy(new_name=None)
        
        shape_movable, shape_fixed = split_shape_by_percentage(half_to_deform, percentage)  

        deformed_movable = noise_callable(shape_movable)


        result = shape_connect_by_index(
            deformed_movable, 
            shape_fixed, 
            len(half_to_deform.points), 
            deformed_movable.name
        )

        shape_to_save = shape_connect(shape, result) 


        d = Drawer()
        d.draw_points(deformed_movable, color="red", size=10)
        d.draw_points(shape_fixed, color="green", size=10)
        d.draw_shape(shape, color="blue", linewidth=2)
        d.draw_shape(result, color="black", linewidth=2)

        d.set_title(f"Random Noise α={alpha} Deformace: {len(shape_movable.points)}/{len(half_to_deform.points)-2} Id={i} ")

        shape_name = shape_to_save.name+f"_{i}.png"

        d.save(shape_name, output_dir)
        
        plt.close(d.fig)

    print(f"Úspěšně vygenerováno a uloženo {num_shapes} obrázků do složky {output_dir}.")