from cube.model import Cube
from solver.FirstBlock import solve_first_block_A_star
test=Cube()
test.Exec("B2 R2 D2 L B2 L2 B2 F2 U2 L' D2 R' B R F U B' L' B L2 B")
# test.Exec("D U L")
test.Print()
solution = solve_first_block_A_star(test)
print("Solution: ", " ".join(solution))
test.Exec(" ".join(solution))
test.Print()
