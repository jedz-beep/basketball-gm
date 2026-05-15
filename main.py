"""Entry point. Opens the game window and runs an integration test on startup.

The integration test (Session 1 Step 5) seeds the database if empty, then reads
back team rosters and prints a summary to stdout. After that, a blank game
window is opened so we can verify pygame works end-to-end.
"""

import sys
from pathlib import Path

import pygame

import config
from database import db
from systems import bootstrap


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
        print(f"{name:<28} {city:<18} {roster:>6} {int(total_salary):>13,}€")
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
    """Run the Session 1 integration test, then open the placeholder window."""
    Path(config.SAVES_DIR).mkdir(exist_ok=True)
    run_integration_test()
    if "--no-window" not in sys.argv:
        open_window()
    return 0


if __name__ == "__main__":
    sys.exit(main())
