import pygame

# tabla meret
ROWS = 6
COLS = 7

# pygame init, font miatt
pygame.init()

# szinek
COLOR_BG = (215, 235, 245)
COLOR_BOARD = (0, 60, 180)
COLOR_EMPTY = (240, 240, 255)
COLOR_P1 = (230, 40, 40)
COLOR_P2 = (250, 230, 40)
COLOR_TEXT = (40, 40, 40)
COLOR_ACCENT = (70, 110, 255)
COLOR_BUTTON = (40, 90, 200)
COLOR_BUTTON_HOVER = (70, 130, 255)
COLOR_BUTTON_TEXT = (250, 250, 250)

# UI
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

BOARD_CELL_SIZE = 80
BOARD_WIDTH = COLS * BOARD_CELL_SIZE
BOARD_HEIGHT = ROWS * BOARD_CELL_SIZE

# fontok
FONT_LARGE = pygame.font.SysFont("arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("arial", 24)
