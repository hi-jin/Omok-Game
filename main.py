from game import reset_game, put_stone, update_game_status, get_game_status, get_board, render
import socket
from communicate import decode_message
from typing import Literal, List
import multiprocessing
import time
from argparse import ArgumentParser


def game_loop(
    socket_port: int,
    screen_mode: Literal["real", "virtual"],
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", socket_port))

    reset_game(screen_mode)

    black_addr = None
    white_addr = None

    print(f"listen on port {socket_port}")

    while True:
        if screen_mode == "real":
            time.sleep(0.3)
        render()
        message, addr = sock.recvfrom(2048)
        message = message.decode()
        # print(f"server received {message}")
        cmd, args = decode_message(message)

        match cmd:
            case "whoami":
                if args[0] == "black":
                    black_addr = addr
                elif args[0] == "white":
                    white_addr = addr
                else:
                    raise ValueError("neither black nor white")
                if black_addr is not None and white_addr is not None:
                    sock.sendto(f"obs {get_board()}".encode(), black_addr)
            case "put":
                if black_addr is None or white_addr is None:
                    raise RuntimeError("black or white isn't registered")
                if addr == black_addr:
                    status = put_stone("black", int(args[0]), int(args[1]))
                    if status != "success":
                        sock.sendto(status.encode(), black_addr)
                        continue
                elif addr == white_addr:
                    status = put_stone("white", int(args[0]), int(args[1]))
                    if status != "success":
                        sock.sendto(status.encode(), white_addr)
                        continue
                else:
                    raise ValueError("white or black not initialized")

                update_game_status()
                match get_game_status():
                    case "black_turn":
                        sock.sendto(f"obs {get_board()}".encode(), black_addr)
                    case "white_turn":
                        sock.sendto(f"obs {get_board()}".encode(), white_addr)
                    case "draw":
                        sock.sendto(f"draw".encode(), black_addr)
                        sock.sendto(f"draw".encode(), white_addr)
                        reset_game(screen_mode)
                        sock.sendto(f"obs {get_board()}".encode(), black_addr)
                    case "black_win":
                        sock.sendto(f"win".encode(), black_addr)
                        sock.sendto(f"lose".encode(), white_addr)
                        reset_game(screen_mode)
                        sock.sendto(f"obs {get_board()}".encode(), black_addr)
                    case "white_win":
                        sock.sendto(f"win".encode(), white_addr)
                        sock.sendto(f"lose".encode(), black_addr)
                        reset_game(screen_mode)
                        sock.sendto(f"obs {get_board()}".encode(), black_addr)


def spawn_games(
    ports: List[int],
    screen_mode: Literal["real", "virtual"],
):
    args = []
    for port in ports:
        args.append((port, screen_mode))
    with multiprocessing.Pool(len(ports)) as p:
        p.starmap(game_loop, args)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--screen-mode", type=str, required=True)
    args = parser.parse_args()

    spawn_games([args.port], args.screen_mode)
