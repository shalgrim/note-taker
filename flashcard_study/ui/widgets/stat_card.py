"""Stat card widget for dashboard."""

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static


class StatCard(Container):
    """A card displaying a single statistic."""

    def __init__(self, label: str, value: str, color: str = "cyan"):
        """Initialize stat card.

        Args:
            label: The stat label (e.g., "Due Today")
            value: The stat value (e.g., "5")
            color: Color name for styling
        """
        super().__init__()
        self.label = label
        self.value = value
        self.color = color
        self.add_class("stat-card")

    def compose(self) -> ComposeResult:
        """Compose the stat card."""
        yield Static(self.value, classes="stat-value")
        yield Static(self.label, classes="stat-label")
