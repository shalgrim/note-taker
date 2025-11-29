"""Configuration constants for flashcard study."""

from pathlib import Path

# File paths
DEFAULT_FLASHCARD_PATH = Path.home() / ".flashcards" / "flashcards.json"

# UI Colors (Dracula-inspired theme)
COLOR_PRIMARY = "#8be9fd"  # Cyan
COLOR_SECONDARY = "#bd93f9"  # Purple
COLOR_SUCCESS = "#50fa7b"  # Green
COLOR_WARNING = "#ffb86c"  # Orange
COLOR_ERROR = "#ff5555"  # Red
COLOR_SURFACE = "#282a36"  # Dark gray
COLOR_BACKGROUND = "#1e1e1e"  # Darker gray

# Default quiz settings
DEFAULT_QUIZ_COUNT = 10

# Mastery thresholds
MASTERY_LEARNING_THRESHOLD = 10  # review_count < 10 = learning
