from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional
from config import ROWS, COLS


class Variant(Enum):
    CLASSIC = "Klasszikus"
    FAST = "Felgyorsított"
    REVERSE = "Fordított"
    FAST_REVERSE = "Felgyorsított + fordított"


# ures tabla letrehozasa
def create_empty_board() -> List[List[int]]:
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


# ellenorzi hogy oszlop ervenyes-e
def is_valid_column(board: List[List[int]], col: int) -> bool:
    return 0 <= col < COLS and board[0][col] == 0


# elerheto oszlopok listaja
def available_columns(board: List[List[int]]) -> List[int]:
    return [c for c in range(COLS) if is_valid_column(board, c)]


# megkeresi a legalso ures sort egy oszlopban
def drop_row_for_col(board: List[List[int]], col: int) -> int:
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return -1


# ellenorzi hogy egy jatekos kirakott-e 4-est
def has_four(board: List[List[int]], player: int) -> bool:
    # vizszintes
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    # fuggoleges
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # atlok
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False


# ellenorzi hogy a tabla tele van-e
def is_full(board: List[List[int]]) -> bool:
    return all(board[0][c] != 0 for c in range(COLS))


# varians alapjan meghatarozza a nyertest
def winner_for_variant(board: List[List[int]], variant: Variant) -> Optional[int]:
    p1 = has_four(board, 1)
    p2 = has_four(board, 2)

    if not p1 and not p2:
        if is_full(board):
            return 0
        return None

    if variant in (Variant.CLASSIC, Variant.FAST):
        if p1 and not p2:
            return 1
        if p2 and not p1:
            return 2
        return 0

    if p1 and not p2:
        return 2
    if p2 and not p1:
        return 1
    return 0


@dataclass
class GameState:
    variant: Variant
    board: List[List[int]] = field(default_factory=create_empty_board)
    player: int = 1
    moves_left_in_turn: int = 1
    game_over: bool = False
    winner: Optional[int] = None

    # inicializalas varians alapjan
    def __post_init__(self):
        if self.variant in (Variant.FAST, Variant.FAST_REVERSE):
            self.moves_left_in_turn = 2
        else:
            self.moves_left_in_turn = 1

    # allapot mely masolata
    def clone(self) -> "GameState":
        return GameState(
            variant=self.variant,
            board=[row[:] for row in self.board],
            player=self.player,
            moves_left_in_turn=self.moves_left_in_turn,
            game_over=self.game_over,
            winner=self.winner,
        )

    # legalis lepesek listazasa
    def legal_moves(self) -> List[int]:
        if self.game_over:
            return []
        return available_columns(self.board)

    # egy lepes alkalmazasa
    def apply_move(self, col: int) -> None:
        if self.game_over:
            return
        if not is_valid_column(self.board, col):
            return

        row = drop_row_for_col(self.board, col)
        if row == -1:
            return

        self.board[row][col] = self.player

        # gyozelem/dontetlen ell.
        w = winner_for_variant(self.board, self.variant)
        if w is not None:
            self.game_over = True
            self.winner = w
            return

        # korvaltas logika
        if self.variant in (Variant.FAST, Variant.FAST_REVERSE):
            if self.moves_left_in_turn > 1:
                self.moves_left_in_turn -= 1
            else:
                self.player = 3 - self.player
                self.moves_left_in_turn = 2
        else:
            self.player = 3 - self.player
            self.moves_left_in_turn = 1
