from dataclasses import dataclass


@dataclass
class Position:
    row: int
    col: int


@dataclass
class TileData:
    letter: str
    blue_value: int
    red_value: int
    selected: bool = False


@dataclass
class LevelState:
    level: int = 1
    target_remaining: int = 0
    turns_used: int = 0
    game_over: bool = False
    win_level: bool = False


@dataclass
class WordState:
    current_word: str = ""
    selected_entities: list[int] | None = None
    message: str = "Forma una palabra y pulsa ENVIAR"

    def __post_init__(self):
        if self.selected_entities is None:
            self.selected_entities = []
