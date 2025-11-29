"""Card list and management screen."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, DataTable, Button, Static

from ...data.repository import FlashCardRepository


class CardListScreen(Screen):
    """Screen for browsing and managing cards."""

    BINDINGS = [
        ("n", "new_card", "New Card"),
        ("e", "edit_card", "Edit"),
        ("d", "delete_card", "Delete"),
        ("escape", "go_back", "Back"),
    ]

    def __init__(self, repository: FlashCardRepository):
        """Initialize card list screen.

        Args:
            repository: FlashCardRepository instance
        """
        super().__init__()
        self.repository = repository

    def compose(self) -> ComposeResult:
        """Compose the card list screen."""
        yield Header()
        yield Container(
            Static("Flash Cards", id="title"),
            DataTable(id="card-table"),
            Horizontal(
                Button("New (n)", id="btn-new", variant="primary"),
                Button("Edit (e)", id="btn-edit"),
                Button("Delete (d)", id="btn-delete", variant="error"),
                Button("Back (Esc)", id="btn-back"),
            ),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Set up the data table."""
        table = self.query_one(DataTable)
        table.add_columns("Question", "Tags", "Reviews", "Ease", "Next Review")

        database = self.repository.load()
        for card in database.cards:
            tags_str = ", ".join(card.tags) if card.tags else ""
            next_review_str = card.next_review.strftime("%Y-%m-%d %H:%M")
            table.add_row(
                card.question[:50] + "..." if len(card.question) > 50 else card.question,
                tags_str,
                str(card.review_count),
                f"{card.ease_factor:.2f}",
                next_review_str,
                key=str(card.id)
            )

        if database.cards:
            table.cursor_type = "row"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-new":
            self.action_new_card()
        elif event.button.id == "btn-edit":
            self.action_edit_card()
        elif event.button.id == "btn-delete":
            self.action_delete_card()
        elif event.button.id == "btn-back":
            self.action_go_back()

    def action_new_card(self) -> None:
        """Create a new card."""
        from .card_form import CardFormScreen
        self.app.push_screen(CardFormScreen(self.repository))

    def action_edit_card(self) -> None:
        """Edit the selected card."""
        table = self.query_one(DataTable)
        if table.cursor_row >= 0:
            row_key = table.get_row_at(table.cursor_row)
            # TODO: Get card by ID and push edit screen
            pass

    def action_delete_card(self) -> None:
        """Delete the selected card."""
        table = self.query_one(DataTable)
        if table.cursor_row >= 0:
            row_key = table.get_row_at(table.cursor_row)
            # TODO: Show confirmation and delete card
            pass

    def action_go_back(self) -> None:
        """Return to home screen."""
        self.app.pop_screen()
