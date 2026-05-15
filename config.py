"""Game-wide constants. Single source for screen, colors, and tuning numbers."""

# --- Display ---
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
FPS = 60
WINDOW_TITLE = "Basketball GM — European Edition"

# --- Theme (dark default; light toggle added in Phase 3) ---
COLOR_BG = (18, 20, 24)
COLOR_SURFACE = (28, 31, 36)
COLOR_TEXT = (235, 238, 242)
COLOR_TEXT_DIM = (150, 158, 168)
COLOR_ACCENT = (255, 138, 0)
COLOR_POSITIVE = (60, 200, 120)
COLOR_NEGATIVE = (230, 70, 80)
COLOR_BORDER = (45, 50, 58)

# --- Attribute system ---
ATTRIBUTE_MIN = 1
ATTRIBUTE_MAX = 20

# --- League: Winner League (Israel) MVP defaults ---
LEAGUE_NAME = "Winner League"
LEAGUE_COUNTRY = "Israel"
LEAGUE_TEAM_COUNT = 12
LEAGUE_REGULAR_SEASON_GAMES = 22  # double round robin
LEAGUE_PLAYOFF_TEAMS = 8
FOREIGN_PLAYER_LIMIT = 5  # active roster non-Israeli cap (Winner League rule)

# --- Roster ---
ROSTER_MIN_SIZE = 10
ROSTER_MAX_SIZE = 14

# --- Seed data sizes ---
SEED_PLAYER_COUNT = 200
SEED_TEAM_COUNT = 12

# --- Database ---
SAVES_DIR = "saves"
DEFAULT_DB_FILENAME = "newgame.db"

# --- Money (euros, league baseline) ---
DEFAULT_TEAM_BUDGET = 4_000_000
MIN_PLAYER_SALARY = 30_000
MAX_PLAYER_SALARY = 800_000

# --- Random seed for reproducible seed-data generation ---
SEED_RANDOM = 42
