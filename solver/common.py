from cube.model import Cube


def get_cube_hash(cube: Cube):
    result = ""
    for face in ["U", "F", "R", "D", "B", "L"]:
        for row in cube.State[face]:
            result += "".join(row)
    return result


def get_sb_hash(cube: Cube):
    EDGE_POSITIONS = {
        "UB": (("U", 0, 1), ("B", 0, 1)),
        "UL": (("U", 1, 0), ("L", 0, 1)),
        "UR": (("U", 1, 2), ("R", 0, 1)),
        "UF": (("U", 2, 1), ("F", 0, 1)),
        "BL": (("B", 1, 2), ("L", 1, 0)),
        "BR": (("B", 1, 0), ("R", 1, 2)),
        "FL": (("F", 1, 0), ("L", 1, 2)),
        "FR": (("F", 1, 2), ("R", 1, 0)),
        "DL": (("D", 1, 0), ("L", 2, 1)),
        "DB": (("D", 2, 1), ("B", 2, 1)),
        "DR": (("D", 1, 2), ("R", 2, 1)),
        "DF": (("D", 0, 1), ("F", 2, 1)),
    }

    CORNER_POSITIONS = {
        "UBL": (("U", 0, 0), ("B", 0, 2), ("L", 0, 0)),
        "UBR": (("U", 0, 2), ("B", 0, 0), ("R", 0, 2)),
        "UFL": (("U", 2, 0), ("F", 0, 0), ("L", 0, 2)),
        "UFR": (("U", 2, 2), ("F", 0, 2), ("R", 0, 0)),
        "BLD": (("B", 2, 2), ("D", 2, 0), ("L", 2, 0)),
        "BRD": (("B", 2, 0), ("D", 2, 2), ("R", 2, 2)),
        "FLD": (("F", 2, 0), ("D", 0, 0), ("L", 2, 2)),
        "FRD": (("F", 2, 2), ("D", 0, 2), ("R", 2, 0)),
    }
    target_edges = {"DR": {"y", "r"}, "FR": {"g", "r"}, "BR": {"b", "r"}}
    target_corners = {"FRD": {"g", "y", "r"}, "BRD": {"b", "y", "r"}}
    piece_states = {}
    for pos_name, facelets in EDGE_POSITIONS.items():
        c1 = cube.State[facelets[0][0]][facelets[0][1]][facelets[0][2]]
        c2 = cube.State[facelets[1][0]][facelets[1][1]][facelets[1][2]]
        current_colors = {c1, c2}
        for target_name, colors in target_edges.items():
            if current_colors == colors:
                piece_states[target_name] = f"{pos_name}_{c1}"
    for pos_name, facelets in CORNER_POSITIONS.items():
        c1 = cube.State[facelets[0][0]][facelets[0][1]][facelets[0][2]]
        c2 = cube.State[facelets[1][0]][facelets[1][1]][facelets[1][2]]
        c3 = cube.State[facelets[2][0]][facelets[2][1]][facelets[2][2]]
        current_colors = {c1, c2, c3}

        for target_name, colors in target_corners.items():
            if current_colors == colors:
                piece_states[target_name] = f"{pos_name}_{c1}"
    ordered_targets = ["DR", "FR", "BR", "FRD", "BRD"]
    return "|".join([piece_states[target] for target in ordered_targets])
