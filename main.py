import random
import math

def merge_line(line: list[int]):
    simplified = [0] * 4
    i = 0
    min_index = 0
    for value in line:
        if value > 0:
            if i > min_index and simplified[i-1] == value:
                simplified[i-1] *= 2
                min_index = i
            else:
                simplified[i] = value
                i += 1
    return simplified
    
def is_mergeable(line: list[int]):
    back_index = -1
    fore_index = 0
    while fore_index < 4:
        if line[fore_index] > 0:
            if (back_index >= 0 and line[fore_index] == line[back_index]) or (fore_index - back_index > 1):
                return True
            back_index = fore_index
        fore_index += 1
    return False

MAX_NUM_LENGTH = 6

LEFT  = (0, 0)
RIGHT = (0, 1)
UP    = (1, 0)
DOWN  = (1, 1)

class Game2048API:
    matrix: list[list[int]] = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    empty_spaces = 16

    def __init__(self):
        self.matrix = [row.copy() for row in self.matrix]
        self.put_random_square()
        self.put_random_square()
    
    def get_random_square(self):
        pos_index = random.randrange(self.empty_spaces)
        for row_i, row in enumerate(self.matrix):
            for column_i, value in enumerate(row):
                if value == 0:
                    if pos_index == 0:
                        return (row_i, column_i)
                    pos_index -= 1

    def put_random_square(self):
        random_square = self.get_random_square()
        random_value = random.choices((2, 4), weights=(9, 1))[0]
        self.matrix[random_square[0]][random_square[1]] = random_value
        self.empty_spaces -= 1
    
    def get_value(self, row_i: int, column_i: int):
        return self.matrix[row_i][column_i]
    def set_value(self, row_i: int, column_i: int, new_value: int):
        self.matrix[row_i][column_i] = new_value
    def get_row(self, row_i: int):
        return self.matrix[row_i]
    def set_row(self, row_i: int, new_row: list[int]):
        self.matrix[row_i] = new_row
    def get_column(self, column_i: int):
        return [self.matrix[row_i][column_i] for row_i in range(4)]
    def set_column(self, column_i: int, new_column: list[int]):
        for row_i in range(4):
            self.set_value(row_i, column_i, new_column[row_i])

    def get_line(self, line_i: int, vertical_flag: bool, reverse_flag: bool):
        line: list[int]
        if vertical_flag:
            line = self.get_column(line_i)
        else:
            line = self.get_row(line_i)
        if reverse_flag:
            line = list(reversed(line))
        return line

    def set_line(self, line_i: int, new_line: list[int], vertical_flag: bool, reverse_flag: bool):
        if reverse_flag:
            new_line = list(reversed(new_line))
        if vertical_flag:
            self.set_column(line_i, new_line)
        else:
            self.set_row(line_i, new_line)

    def check_move(self, vertical_flag: bool, reverse_flag: bool):
        for line_i in range(4):
            if is_mergeable(self.get_line(line_i, vertical_flag, reverse_flag)):
                return True

    def move(self, vertical_flag: bool, reverse_flag: bool):
        for line_i in range(4):
            line = self.get_line(line_i, vertical_flag, reverse_flag)
            new_line = merge_line(line)
            self.empty_spaces += new_line.count(0) - line.count(0)
            self.set_line(line_i, new_line, vertical_flag, reverse_flag)
        self.put_random_square()
    
    def get_possible_moves(self):
        valid_directions = []
        for vertical_flag, reverse_flag in (LEFT, RIGHT, UP, DOWN):
            if self.check_move(vertical_flag, reverse_flag):
                valid_directions.append((vertical_flag, reverse_flag))
        return valid_directions

    def get_matrix_value_string(self, row_i, column_i):
        value = self.get_value(row_i, column_i)
        if value == 0:
            return ''
        return str(value)
    
    def color(self, row_i, column_i):
        value = self.get_value(row_i, column_i)
        if value == 0:
            return ''
        return f"\033[48;5;{int(math.log2(value))}m"


    def __str__(self) -> str:
        lines = []
        lines.append("__" + '___'.join(['_' * MAX_NUM_LENGTH] * 4) + '__')
        for row in range(len(self.matrix)):
            lines.append("|" + '|'.join(self.color(row, index) + ' ' * (MAX_NUM_LENGTH + 2) + '\033[0m' for index in range(4)) + '|')
            lines.append("|" + '|'.join([self.color(row, index) + ' ' + self.get_matrix_value_string(row, index) + ' ' * (MAX_NUM_LENGTH - len(self.get_matrix_value_string(row, index))) + ' ' + '\033[0m' for index in range(4)]) + '|')
            lines.append("|" + '|'.join(self.color(row, index) + '_' * (MAX_NUM_LENGTH + 2) + '\033[0m' for index in range(4)) + '|')
        return '\n'.join(lines)

print("Welcome to 2048!")

game2048api = Game2048API()

print(game2048api)

directions = (UP, DOWN, LEFT, RIGHT)
str_directions = ("up", "down", "left", "right")
char_directions = ("w", "s", "a", "d")

while True:
    possible_moves = game2048api.get_possible_moves()
    if len(possible_moves) == 0:
        print("you have lost!")
        exit()
    possible_indices = [directions.index(direction) for direction in possible_moves]
    direction: tuple[bool, bool] | None = None
    retry = False
    while direction is None:
        if retry:
            print("invalid direction, try again\n")
        entry = input("enter a valid direction (" + ', '.join([str_directions[index] + '/' + char_directions[index] for index in possible_indices]) + "): ").lower().strip()
        direction_index: int = None
        if entry in str_directions:
            direction_index = str_directions.index(entry)
        elif entry in char_directions:
            direction_index = char_directions.index(entry)
        if direction_index in possible_indices:
            direction = directions[direction_index]
        retry = True
    print()

    vertical_flag, reverse_flag = direction
    game2048api.move(vertical_flag, reverse_flag)

    print(game2048api)
    print()

    for row in game2048api.matrix:
        if 2048 in row:
            print("you have won!")