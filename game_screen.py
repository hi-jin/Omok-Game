import pygame
from typing import Literal
import numpy as np


STONE_SIZE: int = 30
STONE_MARGIN: int = 5
LINE_THICKNESS: int = 1
GAME_SIZE: int = 15

_SINGLE_STONE_BOX_LENGTH = STONE_SIZE + STONE_MARGIN * 2
_LINE_COUNT = GAME_SIZE + 1
BOARD_LENGTH: int = _SINGLE_STONE_BOX_LENGTH * GAME_SIZE + _LINE_COUNT * LINE_THICKNESS

WIDTH, HEIGHT = (BOARD_LENGTH, BOARD_LENGTH)


# colors
COLOR_BOARD = pygame.Color(237, 161, 90)
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)


def create_screen(
    mode: Literal["real", "virtual"],
) -> pygame.Surface:
    """
    create virtual or real screen
    """

    width, height = (WIDTH, HEIGHT)
    match mode:
        case "real":
            return pygame.display.set_mode((width, height))
        case "virtual":
            return pygame.Surface((width, height))


def render():
    try:
        pygame.display.flip()
    except pygame.error as e:
        if str(e) == "Display mode not set":
            # maybe expected (may use virtual display)
            pass
        else:
            raise e


def draw_board(
    screen: pygame.Surface,
):
    """
    draw omok board
    """

    # ---------- clear all
    screen.fill(COLOR_BOARD)

    # ---------- vertical line
    start_pos = (0, 0)
    end_pos = (0, HEIGHT)
    dx = LINE_THICKNESS + _SINGLE_STONE_BOX_LENGTH
    for i in range(_LINE_COUNT):
        pygame.draw.line(
            surface=screen,
            color=COLOR_BLACK,
            start_pos=start_pos,
            end_pos=end_pos,
            width=LINE_THICKNESS,
        )
        start_pos = (start_pos[0] + dx, start_pos[1])
        end_pos = (end_pos[0] + dx, end_pos[1])

    # ---------- horizontal line
    start_pos = (0, 0)
    end_pos = (WIDTH, 0)
    dy = LINE_THICKNESS + _SINGLE_STONE_BOX_LENGTH
    for i in range(_LINE_COUNT):
        pygame.draw.line(
            surface=screen,
            color=COLOR_BLACK,
            start_pos=start_pos,
            end_pos=end_pos,
            width=LINE_THICKNESS,
        )
        start_pos = (start_pos[0], start_pos[1] + dy)
        end_pos = (end_pos[0], end_pos[1] + dy)


def draw_stone(
    screen: pygame.Surface,
    x: int,  # idx
    y: int,  # idx
    color: Literal["black", "white"],
):
    unit = LINE_THICKNESS + STONE_SIZE + 2 * STONE_MARGIN
    offset = LINE_THICKNESS + STONE_SIZE // 2 + STONE_MARGIN
    x_coord = x * unit + offset
    y_coord = y * unit + offset
    pygame.draw.circle(
        surface=screen,
        color=COLOR_BLACK if color == "black" else COLOR_WHITE,
        center=(x_coord, y_coord),
        radius=STONE_SIZE // 2,
    )


def get_image(
    screen: pygame.Surface,
) -> np.ndarray:
    """
    get current frame (width, height, 3)
    """
    return pygame.surfarray.array3d(screen)
