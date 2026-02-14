import random
from string import ascii_uppercase

from .components import Position, TileData
from .config import (
    GRID_SIZE,
    LETTER_BLUE_MAX,
    LETTER_BLUE_MIN,
    LETTER_RED_MAX,
    LETTER_RED_MIN,
)
from .ecs import ECSWorld

LETTER_POOL = "AAAAABBCCDDDEEEEEFGGHIIIIIJKKLLLMMMNNÑOOOOPPQRRRRSSSSTTTUUUVWXYZ"


def random_letter() -> str:
    return random.choice(LETTER_POOL if "Ñ" in LETTER_POOL else ascii_uppercase)


def create_tile(world: ECSWorld, row: int, col: int) -> int:
    entity = world.create_entity()
    world.add_component(entity, Position(row=row, col=col))
    world.add_component(
        entity,
        TileData(
            letter=random_letter(),
            blue_value=random.randint(LETTER_BLUE_MIN, LETTER_BLUE_MAX),
            red_value=random.randint(LETTER_RED_MIN, LETTER_RED_MAX),
        ),
    )
    return entity


def spawn_initial_grid(world: ECSWorld) -> None:
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            create_tile(world, row, col)


def compact_and_refill_grid(world: ECSWorld) -> None:
    positions = world.get_component(Position)
    tiles = world.get_component(TileData)

    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for entity, pos in positions.items():
        if entity in tiles:
            board[pos.row][pos.col] = entity

    for col in range(GRID_SIZE):
        stack = [board[row][col] for row in range(GRID_SIZE) if board[row][col] is not None]
        new_col = [None] * (GRID_SIZE - len(stack)) + stack

        for row, entity in enumerate(new_col):
            if entity is not None:
                positions[entity].row = row
                positions[entity].col = col

        missing = GRID_SIZE - len(stack)
        for row in range(missing):
            create_tile(world, row, col)
