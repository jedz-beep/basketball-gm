"""Entry point. Opens the game window and runs an integration test on startup.

Flags:
  --no-window         Skip opening the pygame window (CI / headless runs).
  --simulate-season   Run a full regular season and print final standings.
"""

import sys
from pathlib import Path

import pygame

import config
from database import db
from systems import bootstrap, season


def run_integration_test() -> None:
    """Seed DB if empty, then print every team's roster size and total salary."""
    db.connect()
    db.create_tables()
    if bootstrap.is_database_empty():
        print("Database empty — loading seed data...")
        bootstrap.load_seed_data()
    else:
        print("Database already seeded — skipping load.")

    teams = db.query("SELECT id, name, city FROM teams ORDER BY name")
    print(f"\nLeague: {config.LEAGUE_NAME} ({len(teams)} teams)\n")
    print(f"{'Team':<28} {'City':<18} {'Roster':>6} {'Total Wages':>14}")
    print("-" * 70)
    for team_id, name, city in teams:
        rows = db.query(
            "SELECT COALESCE(SUM(c.salary), 0), COUNT(p.id) "
            "FROM players p "
            "LEFT JOIN contracts c ON c.player_id = p.id AND c.team_id = ? "
            "WHERE p.team_id = ?",
            (team_id, team_id),
        )
        total_salary, roster = rows[0]
        print(f"{name:<28} {city:<18} {roster:>6} {int(total_salary):>13,}")
    print()


def simulate_full_season() -> None:
    """Create a season, generate the schedule, play every game, print standings."""
    league_id = db.query("SELECT id FROM leagues LIMIT 1")[0][0]
    year = 2026

    existing = db.query(
        "SELECT id FROM seasons WHERE league_id = ? AND year = ?", (league_id, year)
    )
    if existing:
        season_id = existing[0][0]
        print(f"Season {year} already exists (id={season_id}). Re-using.")
    else:
        season_id = season.create_season(league_id, year)
        n = season.generate_schedule(season_id)
        print(f"Generated schedule: {n} matches.")

    last_day = season.last_scheduled_day(season_id)
    print(f"Simulating regular season ({last_day} days)...")
    while not season.is_regular_season_complete(season_id):
        season.advance_day(season_id, rng_seed=config.SEED_RANDOM)
    season.end_regular_season(season_id)

    standings = season.compute_standings(season_id)
    _print_standings(standings, year)


def _print_standings(standings: list[dict], year: int) -> None:
    """Render the final regular-season standings to stdout."""
    print(f"\nFinal Standings — Winner League {year}")
    print(f"{'#':>2}  {'Team':<24} {'Abbr':<5} {'W':>3} {'L':>3} "
          f"{'PCT':>6} {'PF':>5} {'PA':>5} {'DIFF':>6}")
    print("-" * 70)
    for rank, row in enumerate(standings, start=1):
        print(
            f"{rank:>2}  {row['name']:<24} {row['abbreviation']:<5} "
            f"{row['wins']:>3} {row['losses']:>3} {row['win_pct']:>6.3f} "
            f"{row['pf']:>5} {row['pa']:>5} {row['diff']:>+6}"
        )
    print()


def open_window() -> None:
    """Open a blank pygame window. Closes on QUIT or ESC."""
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    label = font.render(
        "Basketball GM — Foundation OK. Close window to exit.",
        True,
        config.COLOR_TEXT,
    )
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        screen.fill(config.COLOR_BG)
        screen.blit(label, (40, 40))
        pygame.display.flip()
        clock.tick(config.FPS)
    pygame.quit()


def main() -> int:
    """Run integration test, optionally simulate a season, then open the window."""
    Path(config.SAVES_DIR).mkdir(exist_ok=True)
    run_integration_test()
    if "--simulate-season" in sys.argv:
        simulate_full_season()
    if "--no-window" not in sys.argv:
        open_window()
    return 0


if __name__ == "__main__":
    sys.exit(main())
