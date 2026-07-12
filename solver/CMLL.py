from cube.model import Cube

CMLL_SLOTS = {
    "UFL": (("U", 2, 0), ("F", 0, 0), ("L", 0, 2)),
    "UFR": (("U", 2, 2), ("F", 0, 2), ("R", 0, 0)),
    "UBL": (("U", 0, 0), ("B", 0, 2), ("L", 0, 0)),
    "UBR": (("U", 0, 2), ("B", 0, 0), ("R", 0, 2)),
}

_solved = Cube()
TARGET_CORNERS = {}
for slot_name, facelets in CMLL_SLOTS.items():
    colors = {
        _solved.State[facelets[0][0]][facelets[0][1]][facelets[0][2]],
        _solved.State[facelets[1][0]][facelets[1][1]][facelets[1][2]],
        _solved.State[facelets[2][0]][facelets[2][1]][facelets[2][2]]
    }
    TARGET_CORNERS[slot_name] = colors


def get_cmll_pattern_hash(cube: Cube) -> str:
    slot_order = ["UFL", "UFR", "UBL", "UBR"]
    state_parts = []

    for slot in slot_order:
        facelets = CMLL_SLOTS[slot]
        c_u = cube.State[facelets[0][0]][facelets[0][1]][facelets[0][2]]
        c_f = cube.State[facelets[1][0]][facelets[1][1]][facelets[1][2]]
        c_l = cube.State[facelets[2][0]][facelets[2][1]][facelets[2][2]]
        current_colors = {c_u, c_f, c_l}

        belonging_piece = "UNKNOWN"
        for target_name, target_colors in TARGET_CORNERS.items():
            if current_colors == target_colors:
                belonging_piece = target_name
                break
        
        state_parts.append(f"{slot}_{belonging_piece}_{c_u}")

    return "|".join(state_parts)

SOLVED_CMLL_HASH = get_cmll_pattern_hash(Cube())


CMLL_MACROS = {
    "Skip": "",

    "O_Adjacent_Swap": "R U R' F' R U R' U' R' F R2 U' R'",
    "O_Diagonal_Swap": "R U R' U' R' F R2 U' R' U' R U R' F'",

    "H_Columns": "R U2 R' U' R U R' U' R U R'",
    "H_Rows": "F R U R' U' R U R' U' R U R' U' F'",
    "H_Column": "R' F R U2 R' F' R U F R U R' U F'",
    "H_Row": "U F R U' R' U R U2 R' U' R U R' U' F'",

    "Pi_Right_Bar": "F R U R' U' R U R' U' F'",
    "Pi_Back_Slash": "U F R' F' R U2 R U' R' U R U2 R'",
    "Pi_X_Checkerboard": "U' R' F R U F U' R U R' U' F'",
    "Pi_Forward_Slash": "R U2 R' U' R U R' U2 R' F R F'",
    "Pi_Columns": "U2 R' U R U' R2 F R2 U R' U' F' R",
    "Pi_Left_Bar": "U' R' U' R' F R F' R U' R' U2 R",

    "U_Forward_Slash": "R2 D R' U2 R D' R' U2 R'",
    "U_Back_Slash": "R2 D' R U2 R' D R U2 R",
    "U_Front_Row": "R' U' R U' R' U2 R2 U R' U R U2 R'",
    "U_Rows": "U' F R2 D R' U R D' R2 U' F'",
    "U_X_Checkerboard": "R U R' U' R' F2 R2 U' R' U' R U R' F2",
    "U_Back_Row": "U' F R U R' U' F'",

    "T_Left_Bar": "U' R U R' U' R' F R F'",
    "T_Right_Bar": "U' F R U' R' U R U R' F'",
    "T_Rows": "R U2 R' U' R U' R2 U2 R U R' U R",
    "T_Back_Row": "U R' D R U' R U R' U' R' D' R",
    "T_Front_Row": "R' U R M' U2 R2 F R F' R M'",
    "T_Columns": "R' U R2 D R' M U2 R M' D' R2 U' R",

    "S_Left_Bar": "U R U R' U R U2 R'",
    "S_X_Checkerboard": "U L' U2 L U2 L F' L' F",
    "S_Forward_Slash": "U F R' F' R U2 R U2 R'",
    "S_Right_Bar": "U' R U R' U R' F R F' R U2 R'",
    "S_Columns": "U R U R' U' R' F R F' R U R' U R U2 R'",
    "S_Back_Slash": "U' L U' R' U L' U' R",

    "As_Right_Bar": "U R' U' R U' R' U2 R",
    "As_Columns": "U2 R U2 R' U' R U' R'",
    "As_Back_Slash": "U' F' L F L' U2 L' U2 L",
    "As_X_Checkerboard": "U' R U2 R' U2 R' F R F'",
    "As_Forward_Slash": "U' L' U R U' L U R'",
    "As_Left_Bar": "R' U' R U' R' U R' F R F' U R",

    "L_Mirror": "U2 F R U' R' U' R U R' F'",
    "L_Inverse": "U2 F R' F' R U R U' R'",
    "L_Pure": "R U2 R' U' R U R' U' R U R' U' R U' R'",
    "L_Front_Commutator": "R U R' U R' F R F' U2 R' F R F'",
    "L_Diag": "R' U' R U' F U' R' U' R U F'",
    "L_Back_Commutator": "U2 R U R' U' R' F R2 U' R' U R U R' F'"
}


def solve_cmll(scrambled_cube: Cube) -> str:
    if get_cmll_pattern_hash(scrambled_cube) == SOLVED_CMLL_HASH:
        return ""

    auf_options = ["", "U", "U'", "U2"]

    for pre_auf in auf_options:
        for macro_name, macro_str in CMLL_MACROS.items():
            for post_auf in auf_options:
                
                test_cube = scrambled_cube.copy()
                
                move_sequence = []
                if pre_auf: 
                    move_sequence.append(pre_auf)

                
                move_sequence.append(macro_str)
                
                if post_auf: 
                    move_sequence.append(post_auf)
                
                full_scramble_str = " ".join(move_sequence)
                
                test_cube.Exec(full_scramble_str)
                
                if get_cmll_pattern_hash(test_cube) == SOLVED_CMLL_HASH:
                    print(f"[CMLL] Solved via macro: {macro_name}")
                    return full_scramble_str

    return "-"
