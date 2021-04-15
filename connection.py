from ipaddress import IPv4Address  # mypy
from typing import List, Optional, Tuple

import socket
from requests import get
from game import game
from player import AI, Human, Player, SERVER_REQUIRES_INPUT


class Server:

    def __init__(self, port: int) -> None:
        self._port = port
        self.host = get("https://ifconfig.me/ip").text
        self._conn: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self) -> None:
        self._conn.bind((self.host, self._port))
        self._conn.listen(1)
        self._conn, _ = self._conn.accept()

    def send_to_client(self, msg: str) -> None:
        # 'null byte' to separate messages
        self._conn.send(f"{msg}\0".encode())

    def receive_from_client(self) -> str:
        return self._conn.recv(1024).decode()

    def close_server(self) -> None:
        self._conn.close()


class Client:

    def __init__(self, server_ip: IPv4Address, server_port: int) -> None:
        self._server_ip = server_ip
        self._server_port = server_port
        self._sock: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self) -> None:
        self._sock.settimeout(5)
        self._sock.connect((str(self._server_ip), self._server_port))
        self._sock.settimeout(None)

    def send_to_server(self, msg: str) -> None:
        self._sock.send(f"{msg}".encode())

    def receive_from_server(self) -> str:
        return self._sock.recv(1024).decode()


class Config:

    def __init__(self) -> None:
        self.player1: Player = Human()
        self.player2: Player = Human()

    def _init_players(self, ai_plays: bool) -> Tuple[Player, Player]:
        choice = input("Do you want to start? Y/n [any key]. ")
        self.player1 = Human() if choice.lower() == 'y' \
            or not ai_plays else AI()
        self.player2 = Human() if choice.lower() != 'y' \
            or not ai_plays else AI()

        return (self.player1, self.player2) if choice.lower() == 'y' \
            else (self.player2, self.player1)

    @staticmethod
    def _choose_sides(player: Player, other: Player) -> None:
        while True:
            choice = input("Do you want to be X or O. ").upper()
            if choice in ['X', 'O']:
                player.symbol = choice
                other.symbol = 'O' if choice == 'X' else 'X'
                break

            print("Invalid operation. Choose X or O. ")

    def _config_game(self, ai_plays: bool) -> Tuple[Player, Player, int, int]:
        player, other = self._init_players(ai_plays)
        self._choose_sides(player, other)
        while True:
            height, width = Human().get_correct_players_input(
                "Choose size of playground [height]{whitespace}[width] ")
            if height > 4 and width > 4:
                break

            print("Height and width must be at least 5.")

        return player, other, height, width

    @staticmethod
    def _echo_client(ip: IPv4Address, port: int) -> None:
        client = Client(ip, port)
        client.connect_to_server()

        while True:
            # separate messages by 'null byte'
            for text in client.receive_from_server().split('\0'):
                if text == SERVER_REQUIRES_INPUT:
                    client.send_to_server(input())
                elif text != '':
                    print(text)

    def _echo_server(self, server_player: Player, client_player: Player,
                     port: int) -> None:
        server = Server(port)
        # don't know how to tell mypy that players are subclasses of
        # class 'Player'
        self.player1.set_server_and_client(  # type: ignore
            server, self.player1 is not server_player)
        self.player2.set_server_and_client(  # type: ignore
            server, self.player2 is not server_player)
        print(f"Share this with your friend: ip '{server.host}' "
              f"port: {port}")
        server.start_server()
        server.send_to_client(f"You are player {client_player.symbol}")

    def init_game(self, create: bool, ip: Optional[List[IPv4Address]],
                  port: Optional[List[int]]) -> None:
        ai_plays = not create and ip is None
        if create or ai_plays:
            server_player, client_player, height, width = \
                self._config_game(ai_plays)
            if not ai_plays:
                assert port is not None
                self._echo_server(server_player, client_player, port[0])

            game(height, width, self.player1, self.player2)
        else:
            assert ip is not None and port is not None
            self._echo_client(ip[0], port[0])
