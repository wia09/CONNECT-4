import pygame
import sys

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_BG, COLOR_TEXT,
    COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_BUTTON_TEXT,
    FONT_LARGE, FONT_MED,
)
from logic import Variant
from game import run_game

pygame.init()
pygame.mixer.init()

click_sound = pygame.mixer.Sound("assets/click.mp3")

# megfelelo melyseg kivalasztasa
PERFECT_DEPTH = {
    Variant.CLASSIC: 12,
    Variant.FAST: 8,
    Variant.REVERSE: 12,
    Variant.FAST_REVERSE: 14,
}


def main_menu():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Connect-4 variánsok – AI vs AI")
    clock = pygame.time.Clock()

    buttons = []

    labels = [
        ("Klasszikus (megoldott)", Variant.CLASSIC),
        ("Felgyorsított (2-2 korong / kör)", Variant.FAST),
        ("Fordított (nem szabad nyerni)", Variant.REVERSE),
        ("Felgyorsított + fordított", Variant.FAST_REVERSE),
        ("Kilépés", None),
    ]

    button_width = 600
    button_height = 60
    spacing = 20
    total_height = len(labels) * (button_height + spacing)
    start_y = WINDOW_HEIGHT // 2 - total_height // 2 + 40

    for i, (text, variant) in enumerate(labels):
        x = WINDOW_WIDTH // 2 - button_width // 2
        y = start_y + i * (button_height + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append((rect, text, variant))

    running = True
    while running:
        screen.fill(COLOR_BG)

        # cim
        title = FONT_LARGE.render("Connect-4 variánsok – AI vs AI", True, COLOR_TEXT)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 60))

        subtitle = FONT_MED.render(
            "Válassz játékváltozatot! Mindkét játékos mesterséges intelligencia.",
            True,
            COLOR_TEXT,
        )
        screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 120))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for rect, text, variant in buttons:
            hovered = rect.collidepoint(mouse_x, mouse_y)
            pygame.draw.rect(
                screen,
                COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON,
                rect,
                border_radius=14,
            )
            label = FONT_MED.render(text, True, COLOR_BUTTON_TEXT)
            screen.blit(
                label,
                (rect.x + (rect.width - label.get_width()) // 2,
                 rect.y + (rect.height - label.get_height()) // 2)
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, text, variant in buttons:
                    if rect.collidepoint(event.pos):
                        click_sound.play()
                        if variant is None:
                            running = False
                            break

                        # melyseg, varianstol fugg
                        if variant == Variant.CLASSIC:
                            depth = 3
                        elif variant == Variant.FAST:
                            depth = 4
                        elif variant == Variant.REVERSE:
                            depth = 5
                        elif variant == Variant.FAST_REVERSE:
                            depth = 7
                        else:
                            depth = 5

                        result = run_game(variant, depth=depth)
                        if result == "QUIT":
                            running = False
                            break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu()
