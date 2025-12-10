import os
from datetime import datetime
from logic import GameState, Variant
from ai import best_move_stochastic, TRANSPOSITION


# melyseg valasztasa varians alapjan
def depth_for_variant(variant: Variant) -> int:
    if variant == Variant.CLASSIC:
        return 3
    if variant == Variant.FAST:
        return 4
    if variant == Variant.REVERSE:
        return 3
    if variant == Variant.FAST_REVERSE:
        return 3
    return 4


# logolas
def _log(msg: str, log_file):
    print(msg)
    if log_file is not None:
        log_file.write(msg + "\n")
        log_file.flush()


# szimulaciok futtatasa
def simulate_games(variant: Variant,
                   n_games: int = 20,
                   base_depth: int | None = None,
                   log_file=None):
    if base_depth is None:
        base_depth = depth_for_variant(variant)

    stats = {
        "starter_wins": 0,
        "second_wins": 0,
        "draws": 0,
    }

    for i in range(n_games):
        TRANSPOSITION.clear()

        # kezdo jatekos valtakozik
        starting_player = 1 if i % 2 == 0 else 2
        state = GameState(variant=variant, player=starting_player)

        # jatek futtatasa
        while not state.game_over:

            # FAST varians
            if variant == Variant.FAST:
                if state.player == starting_player:
                    local_depth = max(1, base_depth - 1)
                    local_top_k = 6
                else:
                    local_depth = base_depth + 1
                    local_top_k = 2

                move = best_move_stochastic(
                    state,
                    depth=local_depth,
                    top_k=local_top_k
                )

            # FAST_REVERSE varians
            elif variant == Variant.FAST_REVERSE:
                if state.player == starting_player:
                    local_depth = base_depth + 1
                    local_top_k = 2
                else:
                    local_depth = max(1, base_depth - 1)
                    local_top_k = 6

                move = best_move_stochastic(
                    state,
                    depth=local_depth,
                    top_k=local_top_k
                )

            # REVERSE es klasszikus varians
            else:
                move = best_move_stochastic(state,
                                            depth=base_depth,
                                            top_k=3)

            # nincs lepes, akkor dontetlen
            if move is None:
                state.game_over = True
                state.winner = 0
                break

            state.apply_move(move)

        # statisztika frissítése
        if state.winner == 0 or state.winner is None:
            stats["draws"] += 1
        elif state.winner == starting_player:
            stats["starter_wins"] += 1
        else:
            stats["second_wins"] += 1

        _log(
            f"Játék {i + 1}/{n_games} kész, eddig: "
            f"Kezdő={stats['starter_wins']}, "
            f"Második={stats['second_wins']}, "
            f"Döntetlen={stats['draws']}",
            log_file,
        )

    return stats


# szimulacio CLI modban, log fajlba irassal
def run_simulation_cli(variant: Variant,
                       n_games: int = 20,
                       base_depth: int | None = None):
    os.makedirs("logs", exist_ok=True)

    # idobelyeges logfajl
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logfile_path = f"logs/{variant.name}_{timestamp}.log"

    with open(logfile_path, "w", encoding="utf-8") as log_file:
        _log(f"=== SZIMULÁCIÓ INDUL ===", log_file)
        _log(f"Variáns: {variant.value}", log_file)
        _log(f"Meccsek száma: {n_games}", log_file)
        if base_depth is not None:
            _log(f"Alap mélység: {base_depth}", log_file)

        stats = simulate_games(variant, n_games=n_games,
                               base_depth=base_depth,
                               log_file=log_file)

        _log("\n=== SZIMULÁCIÓ KÉSZ ===", log_file)
        _log(f"Variáns: {variant.value}", log_file)
        _log(f"Lejátszott meccsek: {n_games}", log_file)
        _log(f"Kezdő játékos győzelmek:    {stats['starter_wins']}", log_file)
        _log(f"Második játékos győzelmek:  {stats['second_wins']}", log_file)
        _log(f"Döntetlenek:                {stats['draws']}", log_file)

        if n_games > 0:
            _log(f"Kezdő aránya:    {stats['starter_wins'] / n_games:.2%}", log_file)
            _log(f"Második aránya:  {stats['second_wins'] / n_games:.2%}", log_file)
            _log(f"Döntetlen:       {stats['draws'] / n_games:.2%}", log_file)

    print(f"\nLog fájl: {logfile_path}")


if __name__ == "__main__":
     #run_simulation_cli(Variant.CLASSIC, n_games=50)
     #run_simulation_cli(Variant.FAST, n_games=200)
     #run_simulation_cli(Variant.REVERSE, n_games=300)
     run_simulation_cli(Variant.FAST_REVERSE, n_games=100)
