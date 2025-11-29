"""Command line interface for flashcard study."""

import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime

from .app import FlashcardStudyApp
from .data.repository import FlashCardRepository
from .domain.statistics import StatisticsCalculator
from .domain.anki_exporter import AnkiExporter

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


@app.command()
def export(
    output: Path = typer.Argument(..., help="Output path for .apkg file"),
    deck: str = typer.Option("Claude Code", "--deck", "-d", help="Anki deck name"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Filter by tags (comma-separated)"),
    format: str = typer.Option("anki", "--format", "-f", help="Export format (currently only 'anki')"),
):
    """Export flash cards to Anki format.

    Examples:
        flashcard-study export cards.apkg
        flashcard-study export --deck "Python Study" cards.apkg
        flashcard-study export --tags python,algorithms cards.apkg
        flashcard-study export --deck "Web Dev" --tags javascript,react web.apkg
    """
    if format != "anki":
        console.print(f"[red]Error: Only 'anki' format is currently supported[/red]")
        raise typer.Exit(1)

    # Load cards
    repo = FlashCardRepository()
    db = repo.load()

    if not db.cards:
        console.print("[yellow]No cards to export[/yellow]")
        raise typer.Exit(0)

    # Parse tags filter
    tags_filter = None
    if tags:
        tags_filter = [t.strip() for t in tags.split(",")]

    # Export
    exporter = AnkiExporter(deck_name=deck)
    try:
        count = exporter.export(db.cards, output, tags_filter)

        if count == 0:
            console.print("[yellow]No cards matched the filter criteria[/yellow]")
        else:
            console.print(f"[green]✓ Exported {count} card(s) to {output}[/green]")
            console.print(f"[cyan]  Deck: {deck}[/cyan]")
            if tags_filter:
                console.print(f"[cyan]  Tags: {', '.join(tags_filter)}[/cyan]")
    except Exception as e:
        console.print(f"[red]Error exporting cards: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
