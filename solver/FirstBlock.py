import heapq

from cube.model import Cube
from solver.common import get_cube_hash


def get_first_block_heuristic(cube: Cube):
    wrong_pieces = 0

    if cube.State["D"][1][0] != "y" or cube.State["L"][2][1] != "o":
        wrong_pieces += 1

    if cube.State["F"][1][0] != "g" or cube.State["L"][1][2] != "o":
        wrong_pieces += 1

    if cube.State["B"][1][2] != "b" or cube.State["L"][1][0] != "o":
        wrong_pieces += 1

    if (
        cube.State["F"][2][0] != "g"
        or cube.State["D"][0][0] != "y"
        or cube.State["L"][2][2] != "o"
    ):
        wrong_pieces += 1

    if (
        cube.State["B"][2][2] != "b"
        or cube.State["D"][2][0] != "y"
        or cube.State["L"][2][0] != "o"
    ):
        wrong_pieces += 1

    return wrong_pieces


def solve_first_block_A_star(start_cube) -> str:
    move_pool = [
        "U",
        "UPrime",
        "U2",
        "R",
        "RPrime",
        "R2",
        "F",
        "FPrime",
        "F2",
        "L",
        "LPrime",
        "L2",
        "M",
        "MPrime",
        "M2",
        "B",
        "BPrime",
        "B2",
        "D",
        "DPrime",
        "D2",
    ]

    frontier = []
    counter = 0
    h_start = get_first_block_heuristic(start_cube)

    heapq.heappush(frontier, (h_start, 0, counter, [], "", start_cube))
    explored = set()
    states_evaluated = 0

    print(f"[A*] Search started. Initial H: {h_start}")

    while frontier:
        f, g, _, path, last_move, current_cube = heapq.heappop(frontier)
        states_evaluated += 1

        if states_evaluated % 1000 == 0:
            print(
                f"\r[A*] States: {states_evaluated:<6} | Open: {len(frontier):<6} | g: {g:<2} | h: {f - g:<2}",
                end="",
                flush=True,
            )

        if get_first_block_heuristic(current_cube) == 0:
            print(
                f"\n[A*] Success! Total States: {states_evaluated} | Solved in {g} moves."
            )
            return " ".join(path)

        cube_hash = get_cube_hash(current_cube)
        if cube_hash in explored:
            continue
        explored.add(cube_hash)

        for move in move_pool:
            if last_move and move[0] == last_move[0]:
                continue

            next_cube = current_cube.copy()
            getattr(next_cube, move)()

            next_cube_hash = get_cube_hash(next_cube)
            if next_cube_hash not in explored:
                g_next = g + 1
                h_next = get_first_block_heuristic(next_cube)
                f_next = g_next + 2 * h_next

                counter += 1
                new_path = path + [move]

                heapq.heappush(
                    frontier,
                    (f_next, g_next, counter, new_path, move, next_cube),
                )

    print("\n[A*] No solution found.")
    return "-"
