import pygame
import random

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_BG, COLOR_BOARD, COLOR_EMPTY, COLOR_P1, COLOR_P2,
    COLOR_TEXT, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_BUTTON_TEXT,
    BOARD_CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT,
    FONT_LARGE, FONT_MED, FONT_SMALL,
)
from logic import GameState, Variant
from ai import best_move

pygame.init()
pygame.mixer.init()

click_sound = pygame.mixer.Sound("assets/click.mp3")


def moves_per_turn_for_variant(variant: Variant) -> int:
    # lepesek szama, 1 korben
    if variant in (Variant.FAST, Variant.FAST_REVERSE):
        return 2
    return 1


def draw_board(surface: pygame.Surface, state: GameState, starting_player_internal: int):
    surface.fill(COLOR_BG)

    if starting_player_internal == 1:
        internal_player_1 = 1
        internal_player_2 = 2
        first_color_label = "piros"
        second_color_label = "sárga"
    else:
        internal_player_1 = 2
        internal_player_2 = 1
        first_color_label = "sárga"
        second_color_label = "piros"

    # aktualis korben lepo jatekos sorszama es szine
    if state.player == internal_player_1:
        current_disp_num = 1
        current_color_label = first_color_label
    else:
        current_disp_num = 2
        current_color_label = second_color_label

    # vissza gomb
    back_rect = pygame.Rect(20, 20, 140, 40)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovered = back_rect.collidepoint(mouse_x, mouse_y)
    pygame.draw.rect(
        surface,
        COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON,
        back_rect,
        border_radius=10,
    )
    back_text = FONT_SMALL.render("VISSZA", True, COLOR_BUTTON_TEXT)
    surface.blit(
        back_text,
        (back_rect.x + (back_rect.width - back_text.get_width()) // 2,
         back_rect.y + (back_rect.height - back_text.get_height()) // 2)
    )

    # Cím
    title = FONT_LARGE.render(f"{state.variant.value}", True, COLOR_TEXT)
    surface.blit(
        title,
        (WINDOW_WIDTH // 2 - title.get_width() // 2, 20),
    )

    # statusz szoveg (aktualis kor/gyoztes)
    if not state.game_over:
        moves_per_turn = moves_per_turn_for_variant(state.variant)
        status_text = (
            f"{current_disp_num}. játékos köre "
            f"({current_color_label})  |  Körön belüli lépések: {moves_per_turn}"
        )
        status = FONT_MED.render(status_text, True, COLOR_TEXT)
    else:
        if state.winner == 0 or state.winner is None:
            text = "Döntetlen!"
        else:
            # gyoztes kiirasa
            if state.winner == internal_player_1:
                winner_disp_num = 1
            else:
                winner_disp_num = 2
            text = f"{winner_disp_num}. játékos nyert! ({'piros' if state.winner == 1 else 'sárga'})"
        status = FONT_MED.render(text, True, COLOR_TEXT)

    surface.blit(
        status,
        (WINDOW_WIDTH // 2 - status.get_width() // 2, 80),
    )

    # ki kezdett
    info_text = (
        f"1. játékos (kezdő): {first_color_label}   |   "
        f"2. játékos: {second_color_label}"
    )
    info_surf = FONT_SMALL.render(info_text, True, COLOR_TEXT)
    surface.blit(
        info_surf,
        (WINDOW_WIDTH // 2 - info_surf.get_width() // 2, 120),
    )

    # tabla kirajzolasa (kozep)
    board_x = WINDOW_WIDTH // 2 - BOARD_WIDTH // 2
    board_y = WINDOW_HEIGHT // 2 - BOARD_HEIGHT // 2 + 40

    board_rect = pygame.Rect(board_x, board_y, BOARD_WIDTH, BOARD_HEIGHT)
    pygame.draw.rect(surface, COLOR_BOARD, board_rect, border_radius=12)

    for r in range(len(state.board)):
        for c in range(len(state.board[0])):
            cell_x = board_x + c * BOARD_CELL_SIZE + BOARD_CELL_SIZE // 2
            cell_y = board_y + r * BOARD_CELL_SIZE + BOARD_CELL_SIZE // 2

            val = state.board[r][c]
            if val == 0:
                color = COLOR_EMPTY
            elif val == 1:
                color = COLOR_P1
            else:
                color = COLOR_P2

            pygame.draw.circle(
                surface,
                color,
                (cell_x, cell_y),
                BOARD_CELL_SIZE // 2 - 5,
            )

    return back_rect


def run_game(variant: Variant, depth: int = 5):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Connect-4 variánsok – AI vs AI")

    clock = pygame.time.Clock()
    running = True

    # veletlenul valasztjuk ki, hogy ki kezdjen
    starting_player_internal = random.choice([1, 2])
    state = GameState(variant=variant, player=starting_player_internal)

    move_delay_ms = 400
    last_move_time = 0

    while running:
        back_rect = draw_board(screen, state, starting_player_internal)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                click_sound.play()
                return "BACK"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if back_rect.collidepoint(mx, my):
                    click_sound.play()
                    return "BACK"

        now = pygame.time.get_ticks()
        if not state.game_over and now - last_move_time > move_delay_ms:
            # minden korben az AI valasztja a lepest
            move = best_move(state, depth=depth)
            if move is None:
                # ha nincs legalis dontes, akkor dontetlen
                state.game_over = True
                state.winner = 0
            else:
                state.apply_move(move)

            last_move_time = now

        pygame.display.flip()
        clock.tick(60)
