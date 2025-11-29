"""Home screen with dashboard and navigation."""

from datetime import datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button

from ...data.repository import FlashCardRepository
from ...domain.statistics import StatisticsCalculator
from ..widgets.stat_card import StatCard


class HomeScreen(Screen):
    """Main dashboard showing overview and quick actions."""

    BINDINGS = [
        ("s", "start_quiz", "Start Quiz"),
        ("l", "show_card_list", "Card List"),
        ("n", "new_card", "New Card"),
        ("t", "show_statistics", "Statistics"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, repository: FlashCardRepository):
        """Initialize home screen.

        Args:
            repository: FlashCardRepository instance
        """
        super().__init__()
        self.repository = repository

    def compose(self) -> ComposeResult:
        """Compose the home screen."""
        # Load data and calculate stats
        database = self.repository.load()
        stats = StatisticsCalculator.calculate(database.cards, datetime.now())

        yield Header(show_clock=True)
        yield Container(
            Static("Flash Card Study", id="title"),
            Horizontal(
                StatCard("Due Today", str(stats.cards_due_today), "red"),
                StatCard("Reviewed", str(stats.cards_reviewed_today), "green"),
                StatCard("Streak", f"{stats.review_streak_days}d", "cyan"),
                StatCard("Total", str(stats.total_cards), "blue"),
                id="stats-row"
            ),
            Vertical(
                Button("Start Quiz (s)", id="btn-quiz", variant="primary"),
                Button("Browse Cards (l)", id="btn-list"),
                Button("Create Card (n)", id="btn-create"),
                Button("Statistics (t)", id="btn-stats"),
                id="actions"
            ),
            id="home-container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-quiz":
            self.action_start_quiz()
        elif event.button.id == "btn-list":
            self.action_show_card_list()
        elif event.button.id == "btn-create":
            self.action_new_card()
        elif event.button.id == "btn-stats":
            self.action_show_statistics()

    def action_start_quiz(self) -> None:
        """Launch quiz screen."""
        from .quiz import QuizSetupScreen
        self.app.push_screen(QuizSetupScreen(self.repository))

    def action_show_card_list(self) -> None:
        """Show card list screen."""
        from .card_list import CardListScreen
        self.app.push_screen(CardListScreen(self.repository))

    def action_new_card(self) -> None:
        """Show card form for creating new card."""
        from .card_form import CardFormScreen
        self.app.push_screen(CardFormScreen(self.repository))

    def action_show_statistics(self) -> None:
        """Show statistics screen."""
        from .statistics import StatisticsScreen
        self.app.push_screen(StatisticsScreen(self.repository))

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
