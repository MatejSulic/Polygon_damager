def mirror_x(shape):
    """Vrátí shape zrcadlený přes osu Y (x → -x)."""
    new = shape.clone(shape.name + "_mirrored")

    for p in new.points:
        p.x = -p.x

    return new
