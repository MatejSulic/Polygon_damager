import matplotlib.pyplot as plt
from Controllers.ShapeDrawer import Drawer
from Controllers.ShapeProcessor import get_centroid, mirror_y, shape_connect, shape_connect_by_index, split_shape_by_percentage
from Controllers.FileLoader.FileLoader import load_geometry
from Controllers.transforms.radial_noise import add_radial_noise
from Controllers.transforms.random_noise import add_random_noise
from Models.shape import Shape


def GenerateRadialNoiseShapes(shape: Shape, alpha: float, percentage: float, num_shapes: int, is_area: bool):
    
  
    alpha_str = str(alpha).replace('.', '_') 
    pct_str = int(percentage * 100)           
    
    # Rozlišení výstupní složky pro Area vs. Line
    area_suffix = "_area" if is_area else "_line"
    output_dir = f"radial_noise_per{pct_str}_a{alpha_str}{area_suffix}"

    other_half_template = mirror_y(shape) 
                
    shape_before_transform = shape_connect(shape, other_half_template)
    centroid = get_centroid(shape_before_transform)

    
    # 2. PŘÍPRAVA DEFORMAČNÍHO CALLABLE
    radial_noise_callable = lambda s: add_radial_noise(s, centroid, alpha, lock_edges=False) 


    for i in range(num_shapes):
        
        half_to_deform = other_half_template.copy(new_name=None)
        
        shape_movable, shape_fixed = split_shape_by_percentage(half_to_deform, percentage)  

        deformed_movable = radial_noise_callable(shape_movable)


        result = shape_connect_by_index(
            deformed_movable, 
            shape_fixed, 
            len(half_to_deform.points), 
            deformed_movable.name
        )

        shape_to_save = shape_connect(shape, result) # Spojení čisté poloviny s deformovanou


        d = Drawer()
        
        
        # --- PODMÍNĚNÉ VYKRESLOVÁNÍ ---
        if is_area:
            # Vykreslení vyplněné plochy
            d.draw_shape_filled(shape, color="green")
            d.draw_shape_filled(result, color="green")
           
        else:
            d.draw_points(deformed_movable, color="red", size=10) # Pohyblivá (deformovaná) sada
            d.draw_points(shape_fixed, color="green", size=10)    # Pevná sada
            # Vykreslení obrysu
            d.draw_shape(shape, color="blue", linewidth=2)
            d.draw_shape(result, color="black", linewidth=2)
        # -------------------------------

        # Ujistíme se, že ve výpisu je i info o procentuální deformaci
        d.set_title(f"Radial Noise α={alpha} Deformace: {len(shape_movable.points)}/{len(half_to_deform.points)-2} Id={i} (Area: {is_area})")

        shape_name = shape_to_save.name+f"_{i}.png"

        d.save(shape_name, output_dir)
        
        plt.close(d.fig)

    print(f"Úspěšně vygenerováno a uloženo {num_shapes} obrázků do složky {output_dir}.")


def GenerateRandomNoiseShapes(shape: Shape, alpha: float, percentage: float, num_shapes: int, is_area: bool): # Přidáno is_area
    alpha_str = str(alpha).replace('.', '_') 
    pct_str = int(percentage * 100)           
    
    # Rozlišení výstupní složky pro Area vs. Line
    area_suffix = "_area" if is_area else "_line"
    output_dir = f"random_noise_per{pct_str}_a{alpha_str}{area_suffix}"

    other_half_template = mirror_y(shape) 

    
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
        
        
        # --- PODMÍNĚNÉ VYKRESLOVÁNÍ ---
        if is_area:
            # Vykreslení vyplněné plochy
            d.draw_shape_filled(shape, color="green")
            d.draw_shape_filled(result, color="green")
            
        else:
            d.draw_points(deformed_movable, color="red", size=10)
            d.draw_points(shape_fixed, color="green", size=10)
            # Vykreslení obrysu
            d.draw_shape(shape, color="blue", linewidth=2)
            d.draw_shape(result, color="black", linewidth=2)
        # -------------------------------

        d.set_title(f"Random Noise α={alpha} Deformace: {len(shape_movable.points)}/{len(half_to_deform.points)-2} Id={i} (Area: {is_area})")

        shape_name = shape_to_save.name+f"_{i}.png"

        d.save(shape_name, output_dir)
        
        plt.close(d.fig)

    print(f"Úspěšně vygenerováno a uloženo {num_shapes} obrázků do složky {output_dir}.")