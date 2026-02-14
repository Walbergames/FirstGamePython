from .board import compact_and_refill_grid
from .components import LevelState, Position, TileData, WordState
from .config import BASE_TARGET, MAX_TURNS, TARGET_STEP
from .ecs import ECSWorld


class GameLogic:
    def __init__(self, world: ECSWorld, dictionary_words: set[str]):
        self.world = world
        self.dictionary = dictionary_words

        self.level_state = LevelState(level=1, target_remaining=BASE_TARGET)
        self.word_state = WordState()

    def tile_at(self, row: int, col: int) -> int | None:
        positions = self.world.get_component(Position)
        tiles = self.world.get_component(TileData)
        for entity, pos in positions.items():
            if entity in tiles and pos.row == row and pos.col == col:
                return entity
        return None

    def select_tile(self, entity: int) -> None:
        if self.level_state.game_over:
            return

        tiles = self.world.get_component(TileData)
        if entity not in tiles:
            return
        tile = tiles[entity]
        if tile.selected:
            return

        tile.selected = True
        self.word_state.selected_entities.append(entity)
        self.word_state.current_word += tile.letter

    def undo_last_selection(self) -> None:
        if not self.word_state.selected_entities:
            return
        last = self.word_state.selected_entities.pop()
        tiles = self.world.get_component(TileData)
        if last in tiles:
            tiles[last].selected = False
        self.word_state.current_word = self.word_state.current_word[:-1]

    def clear_selection(self) -> None:
        tiles = self.world.get_component(TileData)
        for eid in self.word_state.selected_entities:
            if eid in tiles:
                tiles[eid].selected = False
        self.word_state.selected_entities.clear()
        self.word_state.current_word = ""

    def submit_word(self) -> None:
        if self.level_state.game_over:
            return

        word = self.word_state.current_word.upper()
        if len(word) < 2:
            self.word_state.message = "La palabra debe tener al menos 2 letras"
            return

        self.level_state.turns_used += 1

        if word not in self.dictionary:
            self.word_state.message = f"'{word}' no está en el diccionario"
            self.clear_selection()
            self._check_end_conditions()
            return

        tiles = self.world.get_component(TileData)
        blue_total = sum(tiles[eid].blue_value for eid in self.word_state.selected_entities if eid in tiles)
        red_total = sum(tiles[eid].red_value for eid in self.word_state.selected_entities if eid in tiles)
        score = blue_total * red_total

        self.level_state.target_remaining -= score

        for eid in self.word_state.selected_entities:
            self.world.remove_entity(eid)

        self.word_state.message = (
            f"{word} válida: azul({blue_total}) x rojo({red_total}) = {score}"
        )
        self.word_state.selected_entities.clear()
        self.word_state.current_word = ""

        compact_and_refill_grid(self.world)
        self._check_end_conditions()

    def _check_end_conditions(self) -> None:
        if self.level_state.target_remaining <= 0:
            self.level_state.level += 1
            self.level_state.turns_used = 0
            self.level_state.target_remaining = BASE_TARGET + (self.level_state.level - 1) * TARGET_STEP
            self.word_state.message = (
                f"¡Nivel superado! Ahora estás en nivel {self.level_state.level}"
            )
            return

        if self.level_state.turns_used >= MAX_TURNS:
            self.level_state.game_over = True
            self.word_state.message = "Perdiste: no alcanzaste el objetivo en 5 jugadas"
