from __future__ import annotations  # mypy
from typing import Optional
import typing
if typing.TYPE_CHECKING:
    from connection import Server
    from game import Coordinate, Coordinates, Playground

from random import randint

SERVER_REQUIRES_INPUT = "CLIENT INPUT"


class Player:

    def __init__(self) -> None:
        self.symbol = ''

    def __str__(self) -> str:
        return f"Player {self.symbol}'s turn."

    def set_symbol(self, symbol: str) -> None:
        self.symbol = symbol

    def move(self, playground: Playground, row: int, col: int) -> bool:
        is_in_range = row < playground.height and col < playground.width
        return is_in_range and playground.set_grid(row, col, self.symbol)


class Human(Player):

    def __init__(self, server: Optional[Server] = None,
                 is_client: bool = False) -> None:
        super().__init__()
        self._server = server
        self._is_client = is_client

    def set_server_and_client(self, server: Server, is_client: bool) -> None:
        self._server = server
        self._is_client = is_client

    def print_msg(self, msg: str, send_to_both_sides: bool = True) -> None:
        if self._server is not None and (send_to_both_sides
                                         or self._is_client):
            self._server.send_to_client(msg)

        if send_to_both_sides or not self._is_client:
            print(msg)

    def receive_input(self, msg: str) -> str:
        if self._server is not None and self._is_client:
            self._server.send_to_client(msg)
            self._server.send_to_client(SERVER_REQUIRES_INPUT)
            inp = self._server.receive_from_client()
        else:
            inp = input(msg)

        return inp

    def get_correct_players_input(self, msg: str) -> Coordinate:
        while True:
            inp = self.receive_input(msg).split()
            if len(inp) != 2:
                self.print_msg("Only 2 values are allowed. ", False)
                continue

            row, col = inp[0], inp[1]
            if not row.isdecimal() or not col.isdecimal():
                self.print_msg("Invalid coordinates. ", False)
                continue

            return int(row), int(col)

    def turn(self, playground: Playground) -> None:
        while True:
            row, col = self.get_correct_players_input(
                "Choose your move [row]{whitespace}[col] ")
            if self.move(playground, row, col):
                break

            self.print_msg("These coordinates are not available. ", False)


class AI(Player):

    @staticmethod
    def print_msg(msg: str) -> None:
        print(msg)

    @staticmethod
    def _get_winning_grid(possible_moves: Coordinates,
                          playground: Playground) -> Optional[Coordinate]:
        for row, col in possible_moves:
            count = 1
            neighbors = playground.get_neighbors_coordinates(row, col)
            for x, y in neighbors:
                if playground.playground[x][y] == ' ':
                    count += 1

            if count >= len(possible_moves):
                return row, col

        return None

    def _win_move(self, playground: Playground) -> Optional[Coordinate]:
        possible_moves = playground.possible_moves()
        if len(possible_moves) > 9:
            return None

        return self._get_winning_grid(possible_moves, playground)

    def turn(self, playground: Playground) -> None:
        possible_win_move = self._win_move(playground)
        if possible_win_move is not None:
            row, col = possible_win_move
        else:
            possible_moves = playground.possible_moves()
            row, col = possible_moves[randint(0, len(possible_moves) - 1)]

        self.move(playground, row, col)
