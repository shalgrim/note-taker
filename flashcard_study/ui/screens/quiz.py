"""Quiz mode screens."""

from datetime import datetime
from textual.app import ComposeResult
from textual.screen import ModalScreen, Screen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input, Label, ProgressBar

from ...data.repository import FlashCardRepository
from ...data.models import FlashCard
from ...domain.card_selector import CardSelector
from ...domain.spaced_repetition import apply_review
from ..widgets.card_display import CardDisplay


class QuizSetupScreen(ModalScreen[dict]):
    """Modal screen for configuring quiz parameters."""

    def compose(self) -> ComposeResult:
        """Compose the quiz setup screen."""
        yield Container(
            Static("Quiz Setup", id="title"),
            Label("Tags (comma-separated, optional):"),
            Input(placeholder="e.g., python,algorithms", id="input-tags"),
            Label("Number of cards:"),
            Input(value="10", id="input-count"),
            Label("Include all cards (not just due):"),
            Horizontal(
                Button("Yes", id="btn-all-yes"),
                Button("No", id="btn-all-no", variant="primary"),
                id="all-buttons"
            ),
            Horizontal(
                Button("Start Quiz", id="btn-start", variant="success"),
                Button("Cancel", id="btn-cancel"),
            ),
            classes="modal-dialog"
        )

    def __init__(self, repository: FlashCardRepository):
        """Initialize quiz setup screen.

        Args:
            repository: FlashCardRepository instance
        """
        super().__init__()
        self.repository = repository
        self.include_all = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-all-yes":
            self.include_all = True
            self.query_one("#btn-all-yes").variant = "primary"
            self.query_one("#btn-all-no").variant = "default"
        elif event.button.id == "btn-all-no":
            self.include_all = False
            self.query_one("#btn-all-yes").variant = "default"
            self.query_one("#btn-all-no").variant = "primary"
        elif event.button.id == "btn-start":
            self.action_start()
        elif event.button.id == "btn-cancel":
            self.dismiss()

    def action_start(self) -> None:
        """Start the quiz with configured parameters."""
        tags_input = self.query_one("#input-tags", Input).value
        count_input = self.query_one("#input-count", Input).value

        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        try:
            count = int(count_input)
        except ValueError:
            count = 10

        # Load cards and select for quiz
        database = self.repository.load()
        selected_cards = CardSelector.select_for_quiz(
            database.cards,
            tags=tags if tags else None,
            count=count,
            include_all=self.include_all
        )

        if not selected_cards:
            # TODO: Show message that no cards are available
            self.dismiss()
        else:
            self.dismiss()
            self.app.push_screen(QuizScreen(selected_cards, self.repository))


class QuizScreen(ModalScreen):
    """Modal screen for quiz mode."""

    BINDINGS = [
        ("space", "reveal_answer", "Show Answer"),
        ("0", "score_wrong", "Wrong"),
        ("5", "score_partial", "Partial"),
        ("1", "score_correct", "Correct"),
        ("escape", "cancel_quiz", "Exit"),
    ]

    def __init__(self, cards: list[FlashCard], repository: FlashCardRepository):
        """Initialize quiz screen.

        Args:
            cards: List of cards to quiz
            repository: FlashCardRepository instance
        """
        super().__init__()
        self.cards = cards
        self.repository = repository
        self.current_index = 0
        self.scores = []
        self.answer_revealed = False

    def compose(self) -> ComposeResult:
        """Compose the quiz screen."""
        total = len(self.cards)
        yield Container(
            ProgressBar(total=total, show_eta=False, id="progress"),
            Static(f"Card {self.current_index + 1} of {total}", id="counter"),
            CardDisplay(self.cards[self.current_index], show_answer=False),
            Horizontal(
                Button("Show Answer (Space)", id="btn-reveal", variant="primary"),
                id="reveal-row"
            ),
            Horizontal(
                Button("Wrong (0)", id="btn-wrong", variant="error", disabled=True),
                Button("Partial (5)", id="btn-partial", variant="warning", disabled=True),
                Button("Correct (1)", id="btn-correct", variant="success", disabled=True),
                id="score-row",
                classes="hidden"
            ),
            id="quiz-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-reveal":
            self.action_reveal_answer()
        elif event.button.id == "btn-wrong":
            self.action_score_wrong()
        elif event.button.id == "btn-partial":
            self.action_score_partial()
        elif event.button.id == "btn-correct":
            self.action_score_correct()

    def action_reveal_answer(self) -> None:
        """Show answer and enable scoring buttons."""
        if self.answer_revealed:
            return

        self.answer_revealed = True
        # Update card display to show answer
        card_display = self.query_one(CardDisplay)
        card_display.set_show_answer(True)

        # Hide reveal button, show scoring buttons
        self.query_one("#reveal-row").add_class("hidden")
        score_row = self.query_one("#score-row")
        score_row.remove_class("hidden")
        for button in score_row.query(Button):
            button.disabled = False

    def action_score_wrong(self) -> None:
        """Record score of 0."""
        self._record_score(0.0)

    def action_score_partial(self) -> None:
        """Record score of 0.5."""
        self._record_score(0.5)

    def action_score_correct(self) -> None:
        """Record score of 1."""
        self._record_score(1.0)

    def _record_score(self, score: float) -> None:
        """Record score and move to next card."""
        current_card = self.cards[self.current_index]
        updated_card = apply_review(current_card, score, datetime.now())

        # Update in database
        database = self.repository.load()
        for i, card in enumerate(database.cards):
            if card.id == updated_card.id:
                database.cards[i] = updated_card
                break
        self.repository.save(database)

        self.scores.append(score)

        # Update progress bar
        progress_bar = self.query_one(ProgressBar)
        progress_bar.advance(1)

        # Move to next card or finish
        self.current_index += 1
        if self.current_index >= len(self.cards):
            self._finish_quiz()
        else:
            self._load_next_card()

    def _load_next_card(self) -> None:
        """Load the next card."""
        self.answer_revealed = False

        # Update counter
        total = len(self.cards)
        self.query_one("#counter", Static).update(
            f"Card {self.current_index + 1} of {total}"
        )

        # Update card display
        card_display = self.query_one(CardDisplay)
        card_display.card = self.cards[self.current_index]
        card_display.set_show_answer(False)

        # Reset buttons
        self.query_one("#reveal-row").remove_class("hidden")
        score_row = self.query_one("#score-row")
        score_row.add_class("hidden")
        for button in score_row.query(Button):
            button.disabled = True

    def _finish_quiz(self) -> None:
        """Finish quiz and show summary."""
        avg_score = sum(self.scores) / len(self.scores) if self.scores else 0
        self.dismiss()
        self.app.push_screen(QuizSummaryScreen(len(self.scores), avg_score))

    def action_cancel_quiz(self) -> None:
        """Cancel quiz and return to home."""
        self.dismiss()


class QuizSummaryScreen(ModalScreen):
    """Modal screen showing quiz summary."""

    def __init__(self, cards_reviewed: int, avg_score: float):
        """Initialize quiz summary screen.

        Args:
            cards_reviewed: Number of cards reviewed
            avg_score: Average score across all cards
        """
        super().__init__()
        self.cards_reviewed = cards_reviewed
        self.avg_score = avg_score

    def compose(self) -> ComposeResult:
        """Compose the summary screen."""
        yield Container(
            Static("Quiz Complete!", id="title"),
            Static(f"\nCards Reviewed: {self.cards_reviewed}"),
            Static(f"Average Score: {self.avg_score:.1%}\n"),
            Button("Done", id="btn-done", variant="success"),
            classes="modal-dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "btn-done":
            self.dismiss()
