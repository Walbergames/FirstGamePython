import pygame

from game.board import spawn_initial_grid
from game.config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.dictionary import load_dictionary
from game.ecs import ECSWorld
from game.systems import GameLogic
from game.ui import UI


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Scrabble Numérico ECS")
    clock = pygame.time.Clock()

    world = ECSWorld()
    spawn_initial_grid(world)
    logic = GameLogic(world, load_dictionary())
    ui = UI()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                logic.undo_last_selection()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ui.submit_button.collidepoint(event.pos):
                    logic.submit_word()
                    continue
                if ui.clear_button.collidepoint(event.pos):
                    logic.clear_selection()
                    continue

                cell = ui.grid_cell_from_mouse(event.pos)
                if cell is not None:
                    row, col = cell
                    entity = logic.tile_at(row, col)
                    if entity is not None:
                        logic.select_tile(entity)

        ui.draw(screen, logic)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
