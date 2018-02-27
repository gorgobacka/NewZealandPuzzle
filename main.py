import copy

class Board(object):

    def __init__(self, x=4, y=None):
        if not y:
            y = x

        self.x = x
        self.y = y
        self.steps = []
        self.stones = {}
        self.background = [[None for i in range(self.x)] for j in range(self.y)]
        self.foreground = [[None for i in range(self.x)] for j in range(self.y)]

    def set_stones(self, stones):
        self.stones = stones

    def stone_sum(self):
        sum = 0
        for symbol in self.stones:
            sum += self.stones[symbol]
        return sum

    def fill_background(self, background):
        self.background = background

    def get_foreground(self):
        return self.foreground

    def get_symbol(self, x, y):
        if self.foreground[y][x]:
            return self.foreground[y][x]
        else:
            return self.background[y][x]

    def check_stone(self, symbol, x, y):
        if x < 0 or x > self.x:
            return False

        if y < 0 or y > self.y:
            return False

        if self.foreground[y][x]:
            return False

        if self.get_symbol(x, y) == symbol:
            return False

        if y > 0:
            if self.get_symbol(x, y - 1) == symbol:
                return False

        if y < self.y - 1:
            if self.get_symbol(x, y + 1) == symbol:
                return False

        if x > 0:
            if self.get_symbol(x - 1, y) == symbol:
                return False

            if y > 0:
                if self.get_symbol(x - 1, y - 1) == symbol:
                    return False

            if y < self.y - 1:
                if self.get_symbol(x - 1, y + 1) == symbol:
                    return False

        if x < self.x - 1:
            if self.get_symbol(x + 1, y) == symbol:
                return False

            if y > 0:
                if self.get_symbol(x + 1, y - 1) == symbol:
                    return False

            if y < self.y - 1:
                if self.get_symbol(x + 1, y + 1) == symbol:
                    return False

        return True

    def insert_stone(self, symbol, x, y):
        if self.check_stone(symbol, x, y):
            self.foreground[y][x] = symbol
            self.steps.append([symbol, x, y])
            return True
        return False

    def print_foreground(self):
        for line in self.get_foreground():
            print(line)
        print()


def traverse_board(board, solutions, processed_foregrounds):
    for symbol in board.stones:
        if board.stones[symbol]:
            for x in range(board.x):
                for y in range(board.y):
                    board_new = copy.deepcopy(board)
                    if board_new.insert_stone(symbol, x, y):
                        board_new.stones[symbol] -= 1

                        if not board_new.get_foreground() in processed_foregrounds:
                            print(board_new.steps)
                            traverse_board(board_new, solutions, processed_foregrounds)
                            processed_foregrounds.append(board_new.get_foreground())

    if not board.stone_sum():
        solutions.append(copy.deepcopy(board))


def main():
    solutions = []
    processed_foregrounds = []

    board_NZ = Board(4)
    stones = {'NZ': 4, 'K': 3, 'B': 3, 'R': 3, 'L': 3}
    board_NZ.fill_background([['R', 'K', 'R', 'L'],
                              ['NZ', 'L', 'NZ', 'B'],
                              ['K', 'B', 'K', 'L'],
                              ['L', 'R', 'NZ', 'B']])
    board_NZ.set_stones(stones)

    traverse_board(board_NZ, solutions, processed_foregrounds)

    if solutions:
        for solution in solutions:
            print(solution.steps)
            print()
            for line in solution.get_foreground():
                print(line)
            print()

if __name__ == "__main__":
    main()
