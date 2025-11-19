from geometry.centroid import symmetric_x_centroid
from geometry.loader import load_geometry
from geometry.point import Point
from transforms.symmetry import mirror_x
from transforms.random_noise import add_random_noise
from transforms.radial_noise import add_radial_noise
from drawer.matplotlib_drawer import Drawer

def main():
    # 1) načtení tvarů ze souboru
    shapes = load_geometry("shapes_clean.txt")
    shape = shapes[list(shapes.keys())[2]]


    centroid = symmetric_x_centroid(shape)
    point_centroid = Point(centroid[0], centroid[1])

    shape_before_transform = mirror_x(shape)
    # 2) pipeline transformací
    result = (
        shape
        .pipe(mirror_x)
        .pipe(lambda s: add_radial_noise(s, max_damage=0.08))
    )

    # 3) vykreslení
    d = Drawer()
    d.draw_shape(shape, color="blue", linewidth=2)  # původní tvar
    d.draw_shape(shape_before_transform, color="gray", linewidth=0.25) # před zásahem šumu    
    d.draw_points(point_centroid, color="red", size=50)  # těžiště    
    d.draw_shape(result, color="black", linewidth=2)     # deformovaný
    d.show()


if __name__ == "__main__":
    main()
