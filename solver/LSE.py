from collections import deque

from cube.model import Cube


def get_full_cube_hash(cube: Cube) -> str:
    hash_parts = []
    for face in ["U", "F", "R", "D", "B", "L"]:
        for row in cube.State[face]:
            hash_parts.append("".join(row))
    return "|".join(hash_parts)


SOLVED_CUBE_HASH = get_full_cube_hash(Cube())


def solve_lse(scrambled_cube: Cube) -> str:
    start_hash = get_full_cube_hash(scrambled_cube)
    if start_hash == SOLVED_CUBE_HASH:
        return ""
    move_pool = ["U", "U'", "U2", "M", "M'", "M2"]
    queue = deque([(scrambled_cube.copy(), [])])
    explored = set()
    explored.add(start_hash)
    while queue:
        current_cube, path = queue.popleft()
        for move in move_pool:
            next_cube = current_cube.copy()
            next_cube.Exec(move)

            next_hash = get_full_cube_hash(next_cube)
            if next_hash == SOLVED_CUBE_HASH:
                solution = " ".join(path + [move])
                return solution
            if next_hash not in explored:
                explored.add(next_hash)
                queue.append((next_cube, path + [move]))

    return "-"
