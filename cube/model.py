class Cube:
    def __init__(self):
        self.State = {
            "U": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
            "F": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
            "R": [["r", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
            "D": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
            "B": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
            "L": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
        }

    def U(self):
        self.State["U"] = [list(x) for x in zip(*self.State["U"][::-1])]
        temp = self.State["F"][0].copy()
        self.State["F"][0] = self.State["R"][0].copy()
        self.State["R"][0] = self.State["B"][0].copy()
        self.State["B"][0] = self.State["L"][0].copy()
        self.State["L"][0] = temp

    def R(self):
        self.State["R"] = [list(x) for x in zip(*self.State["R"][::-1])]
        temp = [self.State["F"][i][2] for i in range(3)]
        for i in range(3):
            self.State["F"][i][2] = self.State["D"][i][2]
            self.State["D"][i][2] = self.State["B"][2 - i][0]
            self.State["B"][2 - i][0] = self.State["U"][i][2]
            self.State["U"][i][2] = temp[i]

    def F(self):
        self.State["F"] = [list(x) for x in zip(*self.State["F"][::-1])]
        temp = self.State["U"][2].copy()
        for i in range(3):
            self.State["U"][2][i] = self.State["L"][2 - i][2]
            self.State["L"][2 - i][2] = self.State["D"][0][2 - i]
            self.State["D"][0][2 - i] = self.State["R"][i][0]
            self.State["R"][i][0] = temp[i]

    def L(self):
        self.State["L"] = [list(x) for x in zip(*self.State["L"][::-1])]
        temp = [self.State["F"][i][0] for i in range(3)]
        for i in range(3):
            self.State["F"][i][0] = self.State["U"][i][0]
            self.State["U"][i][0] = self.State["B"][2 - i][2]
            self.State["B"][2 - i][2] = self.State["D"][i][0]
            self.State["D"][i][0] = temp[i]

    def D(self):
        self.State["D"] = [list(x) for x in zip(*self.State["D"][::-1])]
        temp = self.State["F"][2].copy()
        self.State["F"][2] = self.State["L"][2].copy()
        self.State["L"][2] = self.State["B"][2].copy()
        self.State["B"][2] = self.State["R"][2].copy()
        self.State["R"][2] = temp

    def B(self):
        self.State["B"] = [list(x) for x in zip(*self.State["B"][::-1])]
        temp = self.State["U"][0].copy()
        for i in range(3):
            self.State["U"][0][i] = self.State["R"][i][2]
            self.State["R"][i][2] = self.State["D"][2][2 - i]
            self.State["D"][2][2 - i] = self.State["L"][2 - i][0]
            self.State["L"][2 - i][0] = temp[i]

    def M(self):
        temp = [self.State["F"][i][1] for i in range(3)]
        for i in range(3):
            self.State["F"][i][1] = self.State["U"][i][1]
            self.State["U"][i][1] = self.State["B"][2 - i][1]
            self.State["B"][2 - i][1] = self.State["D"][i][1]
            self.State["D"][i][1] = temp[i]

    def F2(self):
        for _ in range(2):
            self.F()

    def U2(self):
        for _ in range(2):
            self.U()

    def R2(self):
        for _ in range(2):
            self.R()

    def B2(self):
        for _ in range(2):
            self.B()

    def D2(self):
        for _ in range(2):
            self.D()

    def L2(self):
        for _ in range(2):
            self.L()

    def M2(self):
        for _ in range(2):
            self.M()

    def FPrime(self):
        for _ in range(3):
            self.F()

    def UPrime(self):
        for _ in range(3):
            self.U()

    def RPrime(self):
        for _ in range(3):
            self.R()

    def BPrime(self):
        for _ in range(3):
            self.B()

    def DPrime(self):
        for _ in range(3):
            self.D()

    def LPrime(self):
        for _ in range(3):
            self.L()

    def MPrime(self):
        for _ in range(3):
            self.M()

    def Print(self):
        print(" " * 5, *self.State["U"][0])
        print(" " * 5, *self.State["U"][1])
        print(" " * 5, *self.State["U"][2])
        print(
            *self.State["L"][0],
            *self.State["F"][0],
            *self.State["R"][0],
            *self.State["B"][0],
        )
        print(
            *self.State["L"][1],
            *self.State["F"][1],
            *self.State["R"][1],
            *self.State["B"][1],
        )
        print(
            *self.State["L"][2],
            *self.State["F"][2],
            *self.State["R"][2],
            *self.State["B"][2],
        )
        print(" " * 5, *self.State["D"][0])
        print(" " * 5, *self.State["D"][1])
        print(" " * 5, *self.State["D"][2])

    def Exec(self, scramble_str):
        moves = scramble_str.strip().split()

        for move in moves:
            if move.endswith("'"):
                method_name = move[:-1] + "Prime"
            elif move.endswith("2"):
                method_name = move[:-1] + "2"
            else:
                method_name = move

            if hasattr(self, method_name):
                move_method = getattr(self, method_name)
                move_method()
            else:
                print(f"Invalid move: {move}")

    def get_first_block_heuristic(self):
        mismatches = 0

        for r in [1, 2]:
            for c in range(3):
                if self.State["L"][r][c] != "o":
                    mismatches += 1

        if self.State["F"][1][0] != "g":
            mismatches += 1
        if self.State["F"][2][0] != "g":
            mismatches += 1

        if self.State["D"][0][0] != "y":
            mismatches += 1
        if self.State["D"][1][0] != "y":
            mismatches += 1

        if self.State["B"][1][2] != "b":
            mismatches += 1
        if self.State["B"][2][2] != "b":
            mismatches += 1

        return mismatches
