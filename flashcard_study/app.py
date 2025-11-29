"""Main Textual application for flashcard study."""

from pathlib import Path
from textual.app import App
from textual.binding import Binding

from .data.repository import FlashCardRepository
from .ui.screens.home import HomeScreen


class FlashcardStudyApp(App):
    """Main TUI application for flashcard study."""

    CSS_PATH = "ui/styles/app.tcss"

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("question_mark", "help", "Help"),
    ]

    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.repository = FlashCardRepository()

    def on_mount(self) -> None:
        """Set up initial screen."""
        self.push_screen(HomeScreen(self.repository))

    def action_help(self) -> None:
        """Show help information."""
        # TODO: Implement help screen
        pass
