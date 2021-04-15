from typing import List, Tuple, Optional  # mypy
from player import Human, Player


Board = List[List[str]]
Coordinate = Tuple[int, int]
Coordinates = List[Coordinate]


class Playground:

    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.playground = [[' ' for _ in range(width)] for _ in range(height)]
        self.filled_grids = 0  # == sum(all grids) => game over

    def _create_header(self, playground_str: List[str]) -> None:
        playground_str.append(4 * ' ')
        for i in range(self.width):
            playground_str.append(f" {i: <2} ")

        # separator
        playground_str.append("\n   " + self.width * "+---" + "+\n")

    def __str__(self) -> str:
        result: List[str] = []
        self._create_header(result)

        for i, row in enumerate(self.playground):
            result.append(f" {i} |")

            for grid in row:
                result.append(f" {grid} |")

            result.append("\n   " + self.width * "+---" + "+\n")  # separator

        return ''.join(result)

    def grid_exist(self, row: int, col: int) -> bool:
        return -1 < row < self.height and -1 < col < self.width

    def get_neighbors_coordinates(self, row: int,
                                  col: int) -> Coordinates:
        return [(x, y) for x in range(row - 1, row + 2)
                for y in range(col - 1, col + 2)
                if (row, col) != (x, y) and self.grid_exist(x, y)]

    def _fill_borders(self, row: int, col: int) -> None:
        coordinates = self.get_neighbors_coordinates(row, col)
        for x, y in coordinates:
            if self.playground[x][y] == ' ':
                self.playground[x][y] = '*'
                self.filled_grids += 1

    def set_grid(self, row: int, col: int, symbol: str) -> bool:
        if self.playground[row][col] != ' ':
            return False

        self.playground[row][col] = symbol
        self.filled_grids += 1
        self._fill_borders(row, col)

        return True

    def is_over(self) -> bool:
        return self.filled_grids == self.height * self.width

    def possible_moves(self) -> Coordinates:  # for future use (AI)
        return [(row, col) for row in range(self.height)
                for col in range(self.width)
                if self.playground[row][col] == ' ']


class Game:

    def __init__(self, height: int, width: int, player1: Player,
                 player2: Player) -> None:
        self.playground = Playground(height, width)
        self.player1 = player1
        self.player2 = player2

    def _update(self, player: Player) -> None:
        player.print_msg(f"{self.playground}\n{player}")  # type: ignore

    def _half_round(self, player: Player) -> Optional[Player]:
        self._update(player)
        player.turn(self.playground)  # type: ignore
        return player if self.playground.is_over() else None

    def play(self) -> Player:
        winner = None
        while winner is None:
            winner = self._half_round(self.player1)
            if winner is not None:
                break

            winner = self._half_round(self.player2)

        return winner


def game(height: int, width: int, player1: Player, player2: Player) -> None:
    continue_ = True
    while continue_:
        new_game = Game(height, width, player1, player2)
        winner = new_game.play()
        winner.print_msg(str(new_game.playground))  # type: ignore
        winner.print_msg(f"Player {winner.symbol} wins.")  # type: ignore

        msg = "Do you want to play another game? Y/n [any key]. "
        if isinstance(player1, Human) and isinstance(player2, Human):
            continue_ = player1.receive_input(msg).lower() \
                == player2.receive_input(msg).lower() == 'y'
        else:
            continue_ = input(msg).lower() == 'y'
