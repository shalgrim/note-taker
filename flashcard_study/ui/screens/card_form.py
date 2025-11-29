"""Card creation and editing form."""

from datetime import datetime
from uuid import uuid4
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input, TextArea, Label, Select

from ...data.repository import FlashCardRepository
from ...data.models import FlashCard


class CardFormScreen(ModalScreen):
    """Modal screen for creating or editing a card."""

    def __init__(self, repository: FlashCardRepository, card: FlashCard = None):
        """Initialize card form screen.

        Args:
            repository: FlashCardRepository instance
            card: Optional FlashCard to edit (None for new card)
        """
        super().__init__()
        self.repository = repository
        self.card = card
        self.is_edit = card is not None

    def compose(self) -> ComposeResult:
        """Compose the card form."""
        title = "Edit Card" if self.is_edit else "Create New Card"

        yield Container(
            Static(title, id="title"),
            Vertical(
                Label("Type:"),
                Select(
                    [
                        ("Question & Answer", "qa"),
                        ("Cloze Deletion", "cloze"),
                        ("Multiple Choice", "multiple_choice"),
                    ],
                    value=self.card.type if self.card else "qa",
                    id="select-type"
                ),
                Label("Question:"),
                TextArea(
                    self.card.question if self.card else "",
                    id="input-question"
                ),
                Label("Answer:"),
                TextArea(
                    self.card.answer if self.card else "",
                    id="input-answer"
                ),
                Label("Tags (comma-separated):"),
                Input(
                    ", ".join(self.card.tags) if self.card else "",
                    placeholder="e.g., python, algorithms",
                    id="input-tags"
                ),
                classes="form-field"
            ),
            Horizontal(
                Button("Save", id="btn-save", variant="success"),
                Button("Cancel", id="btn-cancel"),
            ),
            classes="modal-dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-save":
            self.action_save()
        elif event.button.id == "btn-cancel":
            self.dismiss()

    def action_save(self) -> None:
        """Save the card."""
        card_type = self.query_one("#select-type", Select).value
        question = self.query_one("#input-question", TextArea).text
        answer = self.query_one("#input-answer", TextArea).text
        tags_input = self.query_one("#input-tags", Input).value

        tags = [t.strip() for t in tags_input.split(",") if t.strip()]

        if not question or not answer:
            # TODO: Show validation error
            return

        if self.is_edit:
            # Update existing card
            updated_card = self.card.model_copy(update={
                "type": card_type,
                "question": question,
                "answer": answer,
                "tags": tags,
            })
            self.repository.update_card(updated_card)
        else:
            # Create new card
            now = datetime.now()
            new_card = FlashCard(
                id=uuid4(),
                type=card_type,
                question=question,
                answer=answer,
                tags=tags,
                created_at=now,
                next_review=now,
                ease_factor=2.5,
                interval_days=0.0,
                review_count=0,
            )
            self.repository.add_card(new_card)

        self.dismiss()
