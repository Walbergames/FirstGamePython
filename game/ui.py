import pygame

from .components import Position, TileData
from .config import (
    ACCENT,
    BG_COLOR,
    BLUE_SCORE_COLOR,
    BUTTON_COLOR,
    BUTTON_HOVER,
    BUTTON_TEXT,
    GAP,
    GRID_LEFT,
    GRID_SIZE,
    GRID_TOP,
    PANEL_COLOR,
    RED_SCORE_COLOR,
    SCREEN_WIDTH,
    TEXT_COLOR,
    TILE_COLOR,
    TILE_SELECTED_COLOR,
    TILE_SIZE,
)


class UI:
    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.SysFont("consolas", 40, bold=True)
        self.font_big = pygame.font.SysFont("consolas", 30, bold=True)
        self.font = pygame.font.SysFont("consolas", 24)
        self.font_small = pygame.font.SysFont("consolas", 20)

        self.submit_button = pygame.Rect(680, 260, 170, 56)
        self.clear_button = pygame.Rect(680, 330, 170, 56)

    def draw(self, screen, logic):
        screen.fill(BG_COLOR)

        self._draw_header(screen, logic)
        self._draw_buttons(screen)
        self._draw_grid(screen, logic)
        self._draw_message(screen, logic.word_state.message)

    def _draw_header(self, screen, logic):
        level = logic.level_state.level
        target = logic.level_state.target_remaining
        turns = logic.level_state.turns_used

        title = self.font_title.render("Scrabble Numérico ECS", True, ACCENT)
        screen.blit(title, (40, 26))

        info = self.font.render(f"Nivel: {level}   Objetivo restante: {target}   Jugadas: {turns}/5", True, TEXT_COLOR)
        screen.blit(info, (42, 90))

        word_panel = pygame.Rect(40, 120, 820, 48)
        pygame.draw.rect(screen, PANEL_COLOR, word_panel, border_radius=8)
        text = self.font_big.render(logic.word_state.current_word or "_", True, TEXT_COLOR)
        screen.blit(text, (54, 130))

    def _draw_buttons(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        submit_color = BUTTON_HOVER if self.submit_button.collidepoint(mouse_pos) else BUTTON_COLOR
        clear_color = BUTTON_HOVER if self.clear_button.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(screen, submit_color, self.submit_button, border_radius=8)
        pygame.draw.rect(screen, clear_color, self.clear_button, border_radius=8)

        submit_txt = self.font.render("ENVIAR", True, BUTTON_TEXT)
        clear_txt = self.font.render("LIMPIAR", True, BUTTON_TEXT)
        screen.blit(submit_txt, (self.submit_button.x + 34, self.submit_button.y + 14))
        screen.blit(clear_txt, (self.clear_button.x + 28, self.clear_button.y + 14))

    def _draw_grid(self, screen, logic):
        positions = logic.world.get_component(Position)
        tiles = logic.world.get_component(TileData)

        for entity, pos in positions.items():
            if entity not in tiles:
                continue
            tile = tiles[entity]
            x = GRID_LEFT + pos.col * (TILE_SIZE + GAP)
            y = GRID_TOP + pos.row * (TILE_SIZE + GAP)
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

            color = TILE_SELECTED_COLOR if tile.selected else TILE_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=8)

            letter = self.font_title.render(tile.letter, True, TEXT_COLOR)
            screen.blit(letter, (x + 36, y + 30))

            blue = self.font_small.render(str(tile.blue_value), True, BLUE_SCORE_COLOR)
            red = self.font_small.render(str(tile.red_value), True, RED_SCORE_COLOR)
            screen.blit(blue, (x + 8, y + 8))
            screen.blit(red, (x + TILE_SIZE - 20, y + 8))

    def _draw_message(self, screen, message: str):
        panel = pygame.Rect(40, 694, 820, 40)
        pygame.draw.rect(screen, PANEL_COLOR, panel, border_radius=8)
        msg = self.font_small.render(message, True, TEXT_COLOR)
        screen.blit(msg, (50, 704))

    def grid_cell_from_mouse(self, mouse_pos):
        mx, my = mouse_pos
        grid_width = GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * GAP
        grid_height = GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * GAP

        if not (GRID_LEFT <= mx <= GRID_LEFT + grid_width and GRID_TOP <= my <= GRID_TOP + grid_height):
            return None

        col = (mx - GRID_LEFT) // (TILE_SIZE + GAP)
        row = (my - GRID_TOP) // (TILE_SIZE + GAP)
        return int(row), int(col)
