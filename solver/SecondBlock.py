import heapq
import json
import os

from cube.model import Cube
from solver.common import get_cube_hash, get_sb_hash

# تابع هیوریستیک شما همچنان برای چک کردن شرط پایان (Goal Test) استفاده می‌شود
PDB_FILE="solver/sb_pdb.json"
if os.path.exists(PDB_FILE):
    with open(PDB_FILE, "r") as f:
        SECOND_BLOCK_PDB = json.load(f)
    print(f"[A* PDB] Loaded {len(SECOND_BLOCK_PDB)} states successfully!")
else:
    raise FileNotFoundError("sb_pdb.json not found! Please run 'python -m solver.generate_sb_pdb' first.")
def get_second_block_heuristic(cube: Cube) -> int:
    current_hash = get_sb_hash(cube)
    return SECOND_BLOCK_PDB.get(current_hash, 13)


def solve_second_block_A_star_with_pdb(start_cube) -> str:
    move_pool = [
        "U", "U'", "U2",
        "R", "R'", "R2",
        "M", "M'", "M2"
    ]

    inverse_moves = {
        "U": "U'", "U'": "U", "U2": "U2",
        "R": "R'", "R'": "R", "R2": "R2",
        "M": "M'", "M'": "M", "M2": "M2"
    }

    h_start = get_second_block_heuristic(start_cube)
    
    if h_start == 0:
        return ""

    frontier = []
    counter = 0
    heapq.heappush(frontier, (h_start, 0, counter, [], "", start_cube))
    
    explored = set()
    states_evaluated = 0

    print(f"[A* PDB] Search started. Exact distance to goal: {h_start} moves.")

    while frontier:
        _, g, _, path, last_move, current_cube = heapq.heappop(frontier)
        states_evaluated += 1

        if get_second_block_heuristic(current_cube) == 0:
            print(f"[A* PDB] Success! States Evaluated: {states_evaluated} | Solved in {g} moves.")
            return " ".join(path)

        cube_hash = get_cube_hash(current_cube)
        if cube_hash in explored:
            continue
        explored.add(cube_hash)

        for move in move_pool:
            if last_move and move[0] == last_move[0]:
                continue

            getattr(current_cube, "Exec")(move)
            next_cube_hash = get_cube_hash(current_cube)

            if next_cube_hash not in explored:
                g_next = g + 1
                h_next = get_second_block_heuristic(current_cube)
                
                f_next = g_next + h_next

                counter += 1
                new_path = path + [move]

                next_cube_copy = current_cube.copy()
                heapq.heappush(
                    frontier,
                    (f_next, g_next, counter, new_path, move, next_cube_copy),
                )

            getattr(current_cube, "Exec")(inverse_moves[move])

    print("\n[A* PDB] No solution found.")
    return "-"
