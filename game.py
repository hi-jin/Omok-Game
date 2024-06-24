from typing import Literal
import numpy as np
from game_screen import GAME_SIZE, draw_stone, draw_board, create_screen, render
import pygame


SCREEN: pygame.Surface = None


GAME_STATUS: Literal[
    "white_turn",
    "black_turn",
    "white_win",
    "black_win",
    "draw",
] = "black_turn"

STONE_EMPTY = 0
STONE_WHITE = 1
STONE_BLACK = 2
BOARD = [[STONE_EMPTY for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]


def reset_game(
    screen_mode: Literal["real", "virtual"],
):
    global SCREEN, GAME_STATUS, BOARD
    if SCREEN is None:
        SCREEN = create_screen(screen_mode)
    BOARD = [[STONE_EMPTY for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
    draw_board(SCREEN)
    GAME_STATUS = "black_turn"


def get_available_action_coords() -> np.ndarray:
    global BOARD
    ndarray_board = np.array(BOARD)
    return ndarray_board == STONE_EMPTY


def put_stone(
    who: Literal["black", "white"],
    x: int,
    y: int,
) -> Literal["success", "invalid_position", "invalid_turn"]:
    global GAME_STATUS, BOARD, STONE_BLACK, STONE_WHITE

    expected_turn = "white_turn" if who == "white" else "black_turn"
    if GAME_STATUS != expected_turn:
        return "invalid_turn"

    available = get_available_action_coords()
    if not available[x][y]:
        return "invalid_position"
    else:
        BOARD[x][y] = STONE_BLACK if who == "black" else STONE_WHITE
        draw_stone(
            screen=SCREEN,
            x=x,
            y=y,
            color=who,
        )

        if GAME_STATUS == "white_turn":
            GAME_STATUS = "black_turn"
        else:
            GAME_STATUS = "white_turn"

        return "success"


def _check_gomoku_win():
    global BOARD, STONE_BLACK, STONE_WHITE, GAME_SIZE, STONE_EMPTY

    board = np.array(BOARD)

    def check_line(line):
        """Check if there are 5 consecutive stones in a line"""
        count = 0
        current = 0
        for stone in line:
            if stone == current and stone != STONE_EMPTY:
                count += 1
                if count == 5:
                    return current
            else:
                count = 1
                current = stone
        return 0

    # Check rows
    for row in board:
        result = check_line(row)
        if result:
            return result

    # Check columns
    for col in board.T:
        result = check_line(col)
        if result:
            return result

    # Check diagonals
    diag_offset = GAME_SIZE - 5
    for diag in range(-diag_offset, diag_offset + 1):
        result = check_line(np.diag(board, diag))
        if result:
            return result
        result = check_line(np.diag(np.fliplr(board), diag))
        if result:
            return result

    return STONE_EMPTY


def get_game_status():
    return GAME_STATUS


def update_game_status():
    global GAME_STATUS
    who_win = _check_gomoku_win()
    if who_win == STONE_BLACK:
        GAME_STATUS = "black_win"
    elif who_win == STONE_WHITE:
        GAME_STATUS = "white_win"


if __name__ == "__main__":
    reset_game("real")
    put_stone("black", 1, 1)
    put_stone("white", 2, 1)
    print(_check_gomoku_win())
    put_stone("black", 1, 2)
    put_stone("white", 2, 2)
    put_stone("black", 1, 3)
    put_stone("white", 2, 4)
    put_stone("black", 1, 4)
    put_stone("white", 2, 6)
    put_stone("black", 1, 5)
    put_stone("white", 2, 8)
    print(_check_gomoku_win())
    render()
    input()
