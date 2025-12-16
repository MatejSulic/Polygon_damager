from ast import Tuple
import numpy as np
from Models.point import Point
from Models.shape import Shape

def shape_connect(shape1, shape2):
    new_name = f"{shape1.name}_plus_{shape2.name}"
    shape = shape1.copy( new_name=new_name)
    shape.points.extend([p.copy() for p in shape2.points])
    return shape


def get_centroid(shape):
    """
    Vrací (cx, cy) – těžiště shape.
    """
    x = [p.x for p in shape.points]
    y = [p.y for p in shape.points]
    cx = np.mean(x)
    cy = np.mean(y)
    return Point(cx, cy)


def mirror_y(shape):

    """Vrátí shape zrcadlený přes osu Y (x → -x)."""
    mirrored_shape = shape.copy(new_name=f"{shape.name}_mirrored_y")

    for p in mirrored_shape.points:
        p.x = -p.x

    return mirrored_shape

def mirror_x(shape):

    """Vrátí shape zrcadlený přes osu X (y → -y)."""

    mirrored_shape = shape.copy(new_name=f"{shape.name}_mirrored_x")

    for p in mirrored_shape.points:
        p.y = -p.y

    return mirrored_shape




import numpy as np
from typing import Tuple
# Předpokládáme import třídy Shape

def split_shape_by_percentage(shape: Shape, movement_pct: float) -> Tuple[Shape, Shape]:
    """
    Rozdělí body tvaru na pohyblivou a pevnou sadu, přičemž první a poslední bod
    jsou VŽDY automaticky zařazeny do pevné sady (zámek okrajů).

    :param shape: Vstupní tvar.
    :param movement_pct: Procento bodů ze STŘEDU tvaru, které se stanou "pohyblivými".
    :returns: Dvojice (Shape_pohyblivá, Shape_pevná).
    """
    if not 0.0 <= movement_pct <= 1.0:
         raise ValueError("movement_pct musí být v rozsahu 0.0 až 1.0.")

    num_points = len(shape.points)
    
    # --- 1. GARANTOVANÝ ZÁMEK OKRAJŮ ---
    # Indexy 0 a N-1 jsou VŽDY pevné.
    if num_points < 3:
        # Nelze rozdělit, pokud jsou jen 1 nebo 2 body, které by byly vždy uzamčeny
        raise ValueError("Tvar musí mít alespoň 3 body pro částečnou deformaci s uzamčenými okraji.")
        
    # Indexy bodů uprostřed (vyloučí 0 a N-1)
    central_indices = np.arange(1, num_points - 1)
    num_central = len(central_indices)
    
    # Vždy pevné body (index 0 a N-1)
    guaranteed_fixed_indices = [0, num_points - 1]
    
    # --- 2. NÁHODNÝ VÝBĚR (jen ze středu) ---
    
    # Počet bodů, které se mají HÝBAT (vybráno ze střední sady)
    num_to_move = int(round(num_central * movement_pct))

    # Náhodné promíchání indexů ze středu
    np.random.shuffle(central_indices) 
    
    # 3. Rozdělení indexů
    moving_indices = central_indices[:num_to_move].tolist()
    
    # Zbytek ze středu + garantovaně pevné
    fixed_from_center = central_indices[num_to_move:].tolist()
    fixed_indices = guaranteed_fixed_indices + fixed_from_center
    
    # 4. Tvorba POHYBLIVÉHO tvaru
    # Body jsou vybírány z původního shape.points, kopírujeme je
    moving_points = [shape.points[i].copy() for i in moving_indices]
    moving_shape = Shape(shape.name + "_per" + str(int(movement_pct * 100)), moving_points, contains_indices=moving_indices)
    
    # 5. Tvorba PEVNÉHO tvaru
    # Zde je klíčové, aby FIXED_POINTS zůstaly v PŮVODNÍM POŘADÍ, 
    # pro kombinaci to není nutné, ale je to dobrá praxe.
    # Proto indexy seřadíme, abychom zjednodušili debug, pokud nefunguje combine_by_index
    fixed_indices.sort() 
    fixed_points = [shape.points[i].copy() for i in fixed_indices]
    fixed_shape = Shape(shape.name + "_fixed", fixed_points, contains_indices=fixed_indices)
    
    return moving_shape, fixed_shape

from typing import Dict
# Předpokládáme, že Shape a Point jsou importovány

def shape_connect_by_index(
    shape_1: Shape, 
    shape_2: Shape, 
    original_length: int,
    original_shape_name: str
) -> Shape:
    """
    Kombinuje body z tvarů shape_1 a shape_2 zpět do jednoho tvaru v původním pořadí,
    na základě jejich 'contains_indices'.

    :param shape_1: První tvar (např. deformovaná část).
    :param shape_2: Druhý tvar (např. pevná část).
    :param original_length: Celková délka výsledného Shape (počet bodů v Shape před rozdělením).
    :param original_shape_name: Jméno původního tvaru pro vytvoření nového jména.
    :returns: Nový Shape s body v původním pořadí.
    """

    
    # 1. Vytvoření mapování (index -> bod) pro rychlé vyhledávání
    # Tato mapa bude sloužit jako zdroj všech bodů
    point_map: Dict[int, Point] = {}

    for shape_part in [shape_1, shape_2]:
        if not shape_part.contains_indices:
             raise ValueError(f"Shape part '{shape_part.name}' nemá definované 'contains_indices'. Nelze kombinovat.")
        
        # Zaplnění mapy: klíč = původní index, hodnota = bod
        for original_index, point in zip(shape_part.contains_indices, shape_part.points):
            if original_index in point_map:
                 # Tohle by nemělo nastat, pokud se indexy nepřekrývají
                 raise RuntimeError(f"Index {original_index} je obsažen ve více částech.")
            point_map[original_index] = point

    # 2. Sestavení finálního seznamu v požadovaném pořadí (0 až N-1)
    combined_points = [None] * original_length 
    
    for i in range(original_length):
        if i not in point_map:
            raise RuntimeError(f"Kombinace selhala: Bod s původním indexem {i} chybí v obou tvarech.")
        
        combined_points[i] = point_map[i]

    # 3. Kontrola (volitelné, ale dobré)
    if None in combined_points:
        # Toto by mělo být pokryto v kroku 2, ale pro jistotu
        raise RuntimeError("Kombinace selhala: Některé sloty zůstaly prázdné.")

    # 4. Vytvoření finálního tvaru
    new_name = original_shape_name
    final_shape = Shape(new_name, combined_points)
    
    return final_shape