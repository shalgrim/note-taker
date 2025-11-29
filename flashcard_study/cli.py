"""Command line interface for flashcard study."""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from datetime import datetime

from .app import FlashcardStudyApp
from .data.repository import FlashCardRepository
from .domain.statistics import StatisticsCalculator

app = typer.Typer(
    name="flashcard-study",
    help="Terminal UI for flash card study with spaced repetition"
)

console = Console()


@app.command()
def main(
    stats: bool = typer.Option(False, "--stats", help="Show statistics and exit"),
    version: bool = typer.Option(False, "--version", help="Show version and exit"),
):
    """Launch the flashcard study TUI application.

    Examples:
        flashcard-study           # Launch TUI
        flashcard-study --stats   # Show stats without launching TUI
    """
    if version:
        from . import __version__
        console.print(f"[cyan]flashcard-study[/cyan] version {__version__}")
        return

    if stats:
        show_quick_stats()
        return

    # Launch TUI
    tui_app = FlashcardStudyApp()
    tui_app.run()


def show_quick_stats() -> None:
    """Display quick statistics in terminal."""
    repo = FlashCardRepository()
    db = repo.load()
    stats = StatisticsCalculator.calculate(db.cards, datetime.now())

    table = Table(title="Flash Card Statistics", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Cards", str(stats.total_cards))
    table.add_row("Due Today", str(stats.cards_due_today))
    table.add_row("Reviewed Today", str(stats.cards_reviewed_today))
    table.add_row("Current Streak", f"{stats.review_streak_days} days")
    table.add_row("Average Ease", f"{stats.average_ease_factor:.2f}")

    console.print(table)


if __name__ == "__main__":
    app()
