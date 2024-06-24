import multiprocessing
from main import game_loop
from typing import Literal
import socket
import time
import ast
import numpy as np


def agent(who: Literal["white", "black"]):
    server = ("localhost", 8000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    time.sleep(1)
    sock.sendto(f"whoami {who}".encode(), server)
    message, addr = sock.recvfrom(2048)
    message = message.decode()
    
    commands = message.split(" ")
    cmd = commands.pop(0)
    args = commands

    if cmd == "obs":
        print(f"{who} received obs")
        board = ast.literal_eval("".join(args))
        print(np.array(board))

        print(f"{who} sends put")
        if who == "black":
            sock.sendto("put 0 0".encode(), server)
        else:
            sock.sendto("put 1 1".encode(), server)


def run(who: Literal["game", "white", "black"]):
    match who:
        case "game":
            game_loop(8000, "real")
        case "white":
            agent("white")
        case "black":
            agent("black")


if __name__ == "__main__":
    with multiprocessing.Pool(3) as p:
        p.map(run, ["game", "white", "black"])
