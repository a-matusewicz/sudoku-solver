from display import display_sudoku_solution
import random, sys
from SAT import SAT
from time import time

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    # random.seed(1)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])
    start = time()
    result = None

    # print(sat.variables)
    # print(sat.clauses)

    # try:
    #     result = sat.gsat()
    #     # print(result)
    # except RecursionError:
    #     print("Recursion limit reached. Solution not reachable by GSAT.")

    result = sat.walk_sat()

    if result:
        sat.write_solution(sol_filename, result)
        print("Solved after visiting {} states".format(sat.states_visited))
        print("Solved in: {} seconds\n".format(time() - start))
        display_sudoku_solution(sol_filename)

    # Handles failure case display
    else:
        print("No solution found after visiting {} states".format(sat.states_visited))
        print("Run time: {} seconds".format(time() - start))
        print("Clauses left unsolved: {}".format(sat.clauses_unsolved))
