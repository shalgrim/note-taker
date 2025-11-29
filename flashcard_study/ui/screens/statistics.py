"""Statistics screen."""

from datetime import datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button

from ...data.repository import FlashCardRepository
from ...domain.statistics import StatisticsCalculator
from ..widgets.stat_card import StatCard


class StatisticsScreen(Screen):
    """Screen showing detailed statistics."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def __init__(self, repository: FlashCardRepository):
        """Initialize statistics screen.

        Args:
            repository: FlashCardRepository instance
        """
        super().__init__()
        self.repository = repository

    def compose(self) -> ComposeResult:
        """Compose the statistics screen."""
        database = self.repository.load()
        stats = StatisticsCalculator.calculate(database.cards, datetime.now())

        yield Header()
        yield Container(
            Static("Statistics", id="title"),
            Horizontal(
                StatCard("Total Cards", str(stats.total_cards), "blue"),
                StatCard("Due Today", str(stats.cards_due_today), "red"),
                StatCard("Due This Week", str(stats.cards_due_this_week), "yellow"),
                StatCard("Reviewed Today", str(stats.cards_reviewed_today), "green"),
                id="stats-row"
            ),
            Horizontal(
                StatCard("Streak", f"{stats.review_streak_days} days", "cyan"),
                StatCard("Avg Ease", f"{stats.average_ease_factor:.2f}", "purple"),
                id="stats-row"
            ),
            Container(
                Static("Mastery Distribution", classes="stat-section-title"),
                Static(f"New: {stats.mastery_distribution['new']}"),
                Static(f"Learning: {stats.mastery_distribution['learning']}"),
                Static(f"Mastered: {stats.mastery_distribution['mastered']}"),
                classes="stat-section"
            ),
            Container(
                Static("Top Tags", classes="stat-section-title"),
                *[
                    Static(f"{tag}: {count}")
                    for tag, count in sorted(
                        stats.tag_distribution.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:10]
                ],
                classes="stat-section"
            ),
            Button("Back (Esc)", id="btn-back"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "btn-back":
            self.action_go_back()

    def action_go_back(self) -> None:
        """Return to home screen."""
        self.app.pop_screen()
