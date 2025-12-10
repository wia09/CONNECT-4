import math
import random
from typing import Callable, Tuple, List

from config import ROWS, COLS
from logic import GameState, Variant, available_columns, is_full, has_four, drop_row_for_col

TRANSPOSITION: dict = {}


# klasszikus ablak ertekelo fuggveny
def _eval_classic_window(window: List[int], player: int, opponent: int) -> int:
    score = 0
    pc = window.count(player)
    oc = window.count(opponent)
    ec = window.count(0)

    if pc == 4:
        score += 100_000
    elif pc == 3 and ec == 1:
        score += 5_000
    elif pc == 2 and ec == 2 and oc == 0:
        score += 300

    if oc == 3 and ec == 1:
        score -= 8_000
    elif oc == 2 and ec == 2 and pc == 0:
        score -= 400

    return score


# klasszikus tabla ertekelo fuggveny
def evaluate_classic(board: List[List[int]], player: int) -> int:
    opponent = 3 - player
    score = 0

    center = COLS // 2
    center_count = sum(1 for r in range(ROWS) if board[r][center] == player)
    score += center_count * 20

    for r in range(ROWS):
        row = board[r]
        for c in range(COLS - 3):
            score += _eval_classic_window(row[c:c + 4], player, opponent)

    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            score += _eval_classic_window(col[r:r + 4], player, opponent)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            score += _eval_classic_window(
                [board[r + i][c + i] for i in range(4)],
                player,
                opponent
            )
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            score += _eval_classic_window(
                [board[r - i][c + i] for i in range(4)],
                player,
                opponent
            )

    return score


# gyorsitott ablak ertekelo fuggveny
def _eval_fast_window(window: List[int], player: int, opponent: int) -> int:
    score = 0
    pc = window.count(player)
    oc = window.count(opponent)
    ec = window.count(0)

    if pc == 4:
        score += 1_000_000
    elif pc == 3 and ec == 1:
        score += 30_000
    elif pc == 2 and ec == 2 and oc == 0:
        score += 5_000

    if oc == 3 and ec == 1:
        score -= 2_000_000
    elif oc == 2 and ec == 2 and pc == 0:
        score -= 400_000

    return score


# gyorsitott tabla ertekelo fuggveny
def evaluate_fast(board: List[List[int]], player: int) -> int:
    opponent = 3 - player
    score = 0

    center = COLS // 2
    center_count = sum(1 for r in range(ROWS) if board[r][center] == player)
    score += center_count * 12

    for r in range(ROWS):
        row = board[r]
        for c in range(COLS - 3):
            score += _eval_fast_window(row[c:c + 4], player, opponent)

    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            score += _eval_fast_window(col[r:r + 4], player, opponent)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            score += _eval_fast_window(
                [board[r + i][c + i] for i in range(4)],
                player,
                opponent
            )
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            score += _eval_fast_window(
                [board[r - i][c + i] for i in range(4)],
                player,
                opponent
            )

    return score


# forditott jatek tabla ertekelo fuggveny
def evaluate_reverse(board: List[List[int]], player: int) -> int:
    opponent = 3 - player
    score = 0

    for r in range(ROWS):
        row = board[r]
        for c in range(COLS - 3):
            w = row[c:c + 4]
            pc = w.count(player)
            oc = w.count(opponent)
            ec = w.count(0)

            if pc == 4:
                score -= 1_000_000
            elif pc == 3 and ec == 1:
                score -= 20_000
            elif pc == 2 and ec == 2 and oc == 0:
                score -= 5_000

            if oc == 3 and ec == 1:
                score += 10_000
            elif oc == 2 and ec == 2 and pc == 0:
                score += 2_000

    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            w = col[r:r + 4]
            pc = w.count(player)
            oc = w.count(opponent)
            ec = w.count(0)

            if pc == 4:
                score -= 1_000_000
            elif pc == 3 and ec == 1:
                score -= 20_000
            elif pc == 2 and ec == 2 and oc == 0:
                score -= 5_000

            if oc == 3 and ec == 1:
                score += 10_000
            elif oc == 2 and ec == 2 and pc == 0:
                score += 2_000

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            w = [board[r + i][c + i] for i in range(4)]
            pc = w.count(player)
            oc = w.count(opponent)
            ec = w.count(0)

            if pc == 4:
                score -= 1_000_000
            elif pc == 3 and ec == 1:
                score -= 20_000
            elif pc == 2 and ec == 2 and oc == 0:
                score -= 5_000

            if oc == 3 and ec == 1:
                score += 10_000
            elif oc == 2 and ec == 2 and pc == 0:
                score += 2_000

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            w = [board[r - i][c + i] for i in range(4)]
            pc = w.count(player)
            oc = w.count(opponent)
            ec = w.count(0)

            if pc == 4:
                score -= 1_000_000
            elif pc == 3 and ec == 1:
                score -= 20_000
            elif pc == 2 and ec == 2 and oc == 0:
                score -= 5_000

            if oc == 3 and ec == 1:
                score += 10_000
            elif oc == 2 and ec == 2 and pc == 0:
                score += 2_000

    return score


# kombinalt tabla ertekelo fuggveny
def evaluate_fast_reverse(board: List[List[int]], player: int) -> int:
    base = evaluate_reverse(board, player)
    opponent = 3 - player
    bonus = 0

    for r in range(ROWS):
        row = board[r]
        for c in range(COLS - 3):
            w = row[c:c + 4]
            if w.count(opponent) == 2 and w.count(0) == 2:
                bonus += 20

    return base + bonus


# megfelelo ertekelo fuggveny valasztasa
def get_eval_fn(variant: Variant) -> Callable[[List[List[int]], int], int]:
    if variant == Variant.CLASSIC:
        return evaluate_classic
    if variant == Variant.FAST:
        return evaluate_fast
    if variant == Variant.REVERSE:
        return evaluate_reverse
    if variant == Variant.FAST_REVERSE:
        return evaluate_fast_reverse
    return evaluate_classic


# azonnali nyero lepes keresese
def find_immediate_winning_move(board: List[List[int]], player: int) -> int | None:
    for col in available_columns(board):
        row = drop_row_for_col(board, col)
        if row == -1:
            continue
        board[row][col] = player
        if has_four(board, player):
            board[row][col] = 0
            return col
        board[row][col] = 0
    return None


# lepesek sorrendje kozeptol kifele
def move_order(board: List[List[int]]) -> List[int]:
    valid = available_columns(board)
    center = COLS // 2
    valid.sort(key=lambda c: abs(c - center))
    return valid


# minimax kereses alfa beta vagassal
def minimax(state: GameState,
            depth: int,
            alpha: float,
            beta: float,
            maximizing_player: int,
            eval_fn: Callable[[List[List[int]], int], int]) -> Tuple[int, int]:
    if depth == 0 or state.game_over:
        if state.game_over:
            if state.winner == maximizing_player:
                return 1_000_000 + depth, -1
            elif state.winner == 0 or state.winner is None:
                return 0, -1
            else:
                return -1_000_000 - depth, -1
        else:
            return eval_fn(state.board, maximizing_player), -1

    if not state.legal_moves() and is_full(state.board):
        return 0, -1

    board_key = tuple(tuple(row) for row in state.board)
    key = (
        board_key,
        state.player,
        state.moves_left_in_turn,
        depth,
        maximizing_player,
        state.variant.value,
    )
    if key in TRANSPOSITION:
        return TRANSPOSITION[key]

    valid_moves = state.legal_moves()
    if not valid_moves:
        return 0, -1

    ordered_moves = [c for c in move_order(state.board) if c in valid_moves]
    maximizing = (state.player == maximizing_player)

    if maximizing:
        value = -math.inf
        best_col = ordered_moves[0]
        for col in ordered_moves:
            nxt = state.clone()
            nxt.apply_move(col)
            score, _ = minimax(
                nxt,
                depth - 1,
                alpha,
                beta,
                maximizing_player,
                eval_fn,
            )
            if score > value:
                value = score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        TRANSPOSITION[key] = (value, best_col)
        return value, best_col

    else:
        value = math.inf
        best_col = ordered_moves[0]
        for col in ordered_moves:
            nxt = state.clone()
            nxt.apply_move(col)
            score, _ = minimax(
                nxt,
                depth - 1,
                alpha,
                beta,
                maximizing_player,
                eval_fn,
            )
            if score < value:
                value = score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break

        TRANSPOSITION[key] = (value, best_col)
        return value, best_col


# determinisztikus legjobb lepes keresese
def best_move(state: GameState, depth: int = 7) -> int | None:
    win_col = find_immediate_winning_move(state.board, state.player)
    if win_col is not None:
        return win_col

    opponent = 3 - state.player
    block_col = find_immediate_winning_move(state.board, opponent)
    if block_col is not None:
        return block_col

    TRANSPOSITION.clear()
    eval_fn = get_eval_fn(state.variant)

    _, col = minimax(
        state,
        depth,
        -math.inf,
        math.inf,
        maximizing_player=state.player,
        eval_fn=eval_fn,
    )
    if col == -1:
        return None
    return col


# sztochasztikus legjobb lepes szimulaciohoz
def best_move_stochastic(state: GameState,
                         depth: int = 4,
                         top_k: int = 3) -> int | None:
    legal = state.legal_moves()
    if not legal:
        return None

    win_col = find_immediate_winning_move(state.board, state.player)
    if win_col is not None:
        return win_col

    opponent = 3 - state.player
    block_col = find_immediate_winning_move(state.board, opponent)
    if block_col is not None:
        return block_col

    eval_fn = get_eval_fn(state.variant)
    maximizing_player = state.player
    scored_moves: List[Tuple[int, float]] = []

    for col in move_order(state.board):
        if col not in legal:
            continue
        nxt = state.clone()
        nxt.apply_move(col)

        score, _ = minimax(
            nxt,
            depth - 1,
            -math.inf,
            math.inf,
            maximizing_player=maximizing_player,
            eval_fn=eval_fn,
        )
        scored_moves.append((col, score))

    if not scored_moves:
        return None

    scored_moves.sort(key=lambda x: x[1], reverse=True)
    k = min(top_k, len(scored_moves))
    candidates = [col for col, _ in scored_moves[:k]]

    return random.choice(candidates)
