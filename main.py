from cube.model import Cube
from solver.CMLL import solve_cmll
from solver.FirstBlock import solve_first_block_A_star
from solver.LSE import solve_lse
from solver.SecondBlock import solve_second_block_A_star_with_pdb

test = Cube()
test.Exec("L F' D L2 B2 D' F2 R2 F2 U2 R2 U B2 D' L F D2 L2 R' D2 U2")
# test.Exec("D U L")
test.Print()
full_solution = ""
solution = solve_first_block_A_star(test)
if solution != "-":
    full_solution += solution
    print("First Block: ", solution)
    test.Exec(solution)
    test.Print()
    solution = solve_second_block_A_star_with_pdb(test)
    if solution != "-":
        full_solution = full_solution + " " + solution
        print("Second Block: ", solution)
        test.Exec(solution)
        test.Print()
        solution = solve_cmll(test)
        if solution != "-":
            full_solution = full_solution + " " + solution
            print("CMLL: ", solution)
            test.Exec(solution)
            test.Print()
            solution = solve_lse(test)
            if solution != "-":
                full_solution = full_solution + " " + solution
                print("LSE: ", solution)
                test.Exec(solution)
                test.Print()
                print("Full Solution: ", full_solution)
