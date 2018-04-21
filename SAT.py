import random


class SAT:
    def __init__(self, puzzle):
        self.clauses = []
        self.variables = tuple()
        self.sort_clauses(puzzle)
        self.states_visited = 0         # Keeps track of to note efficiency
        self.clauses_unsolved = 0       # Used in case of failure and for testing

    # Reads a .cnf file to determine variables and clauses
    def sort_clauses(self, puzzle):
        var = []
        with open(puzzle, "r") as f:
            for line in f:
                # Removes new lines from clause list
                line = line.replace("\n", "")
                clause = line.split(" ")
                while "" in clause:
                    clause.remove("")

                new_clause = set()
                negative = False
                for c in clause:
                    edit = c
                    if c[0] == "-":
                        edit = c[1:]
                        negative = True
                    # edit = abs(c)
                    # However, would work with non-numerical variables
                    if edit not in var:
                        var.append(edit)

                    # No zero values for the variable names
                    if negative:
                        new_clause.add(-1 * (var.index(edit) + 1))
                    else:
                        new_clause.add(var.index(edit) + 1)

                self.clauses.append(new_clause)

            self.variables = tuple(var)

    # WalkSAT Algorithm
    def walk_sat(self, p=.3, max_flips=100000):
        # Start with a random model
        model = self.get_rand_model()

        # Until max_flips is reached
        for i in range(max_flips):
            self.states_visited += 1

            # If answer is correct return translated model
            solved = self.is_answer(model)
            if solved:
                return self.translate_back(model)

            # Find the unsolved clauses
            self.clauses_unsolved = 0
            union = self.get_union_set(model)
            clause = random.choice(union)
            # Uncomment below for testing
            # print(self.clauses_unsolved)

            rando = random.random()
            # Random flip
            if rando < p:
                random_bit = random.choice(list(clause))
                model.remove(-1 * random_bit)
                model.add(random_bit)

            # Flip best choice in candidate set
            else:
                scores = {}
                for var in clause:
                    model_temp = set(model)
                    model_temp.remove(-1 * var)
                    model_temp.add(var)

                    score = self.count_corr_clauses(model_temp)
                    # score is key for a list of bits
                    if score in scores:
                        scores[score].append(var)
                    else:
                        scores[score] = [var]

                # Get the highest scoring bit
                sort = sorted(scores.keys(), reverse=True)
                highest_bit = random.choice(scores[sort[0]])

                model.remove(-1 * highest_bit)
                model.add(highest_bit)
        return False

    # Creates a list of clause sets using the disjoint function
    def get_union_set(self, model):
        union = []
        for clause in self.clauses:
            if clause.isdisjoint(model):
                union.append(clause)
                self.clauses_unsolved += 1

        return union

    # GSAT Algorithm
    def gsat(self, threshold=.3, starter=None):
        # Can have a given model for testing
        if starter:
            model = starter
        else:
            model = self.get_rand_model()

        answer = self.gsat_helper(model, threshold)
        return self.translate_back(answer)

    # Helper method for recursion in GSAT
    def gsat_helper(self, model, threshold):
        # If solved then return
        self.states_visited += 1
        solved = self.is_answer(model)
        if solved:
            return model

        rand = random.random()
        # Flip random bit and recheck model
        if rand < threshold:
            random_bit = random.choice(list(model))
            model.remove(random_bit)
            model.add(-1 * random_bit)

            return self.gsat_helper(model, threshold)

        # Flips best bit out of all the variables
        else:
            scores = {}
            for var in model:
                model_temp = set(model)
                model_temp.remove(var)
                model_temp.add(-1 * var)

                score = self.count_corr_clauses(model_temp)
                # score is key for a list of bits
                if score in scores:
                    scores[score].append(var)
                else:
                    scores[score] = [var]

            # Get the highest scoring bit
            sort = sorted(scores.keys(), reverse=True)
            highest_bit = random.choice(scores[sort[0]])

            model.remove(highest_bit)
            model.add(-1 * highest_bit)

            return self.gsat_helper(model, threshold)

    # Returns a random model to begin SAT
    def get_rand_model(self):
        model = set()

        for var in self.variables:
            rando = random.random()
            if rando < .5:
                model.add(-1 * (self.variables.index(var) + 1))
            else:
                model.add(self.variables.index(var) + 1)

        return model

    # Counts fulfilled clauses
    def count_corr_clauses(self, model):
        count = 0
        for clause in self.clauses:
            if not clause.isdisjoint(model):
                count += 1

        return count

    # True if all clauses are satisfied
    def is_answer(self, model):
        solved = True
        for clause in self.clauses:
            if clause.isdisjoint(model):
                solved = False

        return solved

    # Translates solution back into cnf format
    def translate_back(self, answer):
        sol = []
        for a in answer:
            if a == abs(a):
                sol.append(self.variables[a - 1])  # Takes into account initial shift
            else:
                sol.append("-" + self.variables[abs(a) - 1])

        return sol

    # Writes solution (.sol) file
    def write_solution(self, file_name, result):
        with open(file_name, "w") as f:
            f.write(str(result[0]))
            for bit in result:
                f.write("\n" + str(bit))

if __name__ == "__main__":
    sat = SAT("test.cnf")

    model_a = {1, 2, -3, -4, -5, -6, -7, -8, -9}

    check_ans = sat.is_answer(model_a)
    print(check_ans)

    ans = sat.walk_sat()
    print(ans)

    # check_count = sat.count_corr_clauses(model_a, -1)
    # print(check_count)
    # c = sat.get_union_set(model_a)
    # print(model_a)
    # print(c)
    # x = random.choice(c)
    #
    # scores = {}
    # for var in x:  # c[len(c) - 1]:
    #     # print(var)
    #     # self.clauses_unsolved = 0
    #     model_temp = set(model_a)
    #     model_temp.remove(-1 * var)
    #     model_temp.add(var)
    #
    #     score = sat.count_corr_clauses(model_temp, var)
    #     # if score > self.clauses_unsolved:
    #     if score in scores:
    #         scores[score].append(var)
    #     else:
    #         scores[score] = [var]
    #
    # sort = sorted(scores.keys(), reverse=True)
    # highest_bit = random.choice(scores[sort[0]])
    # # print(highest_bit)
    # model_a.remove(-1 * highest_bit)
    # model_a.add(highest_bit)
    #
    # print(highest_bit)
    # print(scores)
    # print(model_a)
