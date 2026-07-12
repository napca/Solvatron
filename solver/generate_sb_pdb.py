import json
from collections import deque

from cube.model import Cube
from solver.common import get_sb_hash



def generate_pdb():
    move_pool = ["U", "UPrime", "U2", "R", "RPrime", "R2", "M", "MPrime", "M2"]
    inverse_moves = {
        "U": "UPrime", "UPrime": "U", "U2": "U2",
        "R": "RPrime", "RPrime": "R", "R2": "R2",
        "M": "MPrime", "MPrime": "M", "M2": "M2"
    }

    solved_cube = Cube()
    start_hash = get_sb_hash(solved_cube)

    pdb = {start_hash: 0}
    queue = deque([(solved_cube, 0, "")])

    print("⏳ Building TRUE Second Block Pattern Database (PDB)...")

    while queue:
        current_cube, depth, last_move = queue.popleft()

        if len(pdb) % 5000 == 0:
            print(f"\r[PDB Generator] Discovered States: {len(pdb)} | Current Depth: {depth}", end="", flush=True)

        for move in move_pool:
            if last_move and move[0] == last_move[0]:
                continue

            getattr(current_cube, move)()
            next_hash = get_sb_hash(current_cube)

            if next_hash not in pdb:
                pdb[next_hash] = depth + 1
                queue.append((current_cube.copy(), depth + 1, move))

            getattr(current_cube, inverse_moves[move])()

    print(f"\n✅ Done! Total unique configurations found: {len(pdb)}")
    
    with open("solver/sb_pdb.json", "w") as f:
        json.dump(pdb, f)
    print("💾 Database saved successfully to 'solver/sb_pdb.json'")

if __name__ == "__main__":
    generate_pdb()
