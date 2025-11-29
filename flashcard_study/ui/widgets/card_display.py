"""Widget for displaying flash cards."""

import re
from textual.widgets import Static
from rich.text import Text

from ...data.models import FlashCard


class CardDisplay(Static):
    """Display card question and optionally answer."""

    def __init__(self, card: FlashCard, show_answer: bool = False):
        """Initialize card display.

        Args:
            card: The flash card to display
            show_answer: Whether to show the answer
        """
        super().__init__()
        self.card = card
        self.show_answer = show_answer
        self.add_class("card-display")

    def render(self) -> Text:
        """Render card based on type."""
        if self.card.type == "qa":
            return self._render_qa()
        elif self.card.type == "cloze":
            return self._render_cloze()
        else:
            return self._render_multiple_choice()

    def _render_qa(self) -> Text:
        """Render Q&A card."""
        content = Text()
        content.append("Question:\n", style="bold cyan")
        content.append(self.card.question + "\n\n")

        if self.show_answer:
            content.append("Answer:\n", style="bold green")
            content.append(self.card.answer)

        return content

    def _render_cloze(self) -> Text:
        """Render cloze deletion card."""
        content = Text()

        if self.show_answer:
            # Highlight the answer
            pattern = r'\{\{(.+?)\}\}'
            parts = re.split(pattern, self.card.question)

            for i, part in enumerate(parts):
                if i % 2 == 1:  # This is the answer part
                    content.append(part, style="bold green on #3a3a3a")
                else:
                    content.append(part)
        else:
            # Replace with blanks
            text = re.sub(r'\{\{.+?\}\}', '_____', self.card.question)
            content.append(text)

        return content

    def _render_multiple_choice(self) -> Text:
        """Render multiple choice card."""
        content = Text()
        content.append(self.card.question + "\n\n", style="bold")

        if self.card.options:
            for i, option in enumerate(self.card.options, 1):
                if self.show_answer and option == self.card.answer:
                    content.append(f"{i}. {option}\n", style="bold green")
                else:
                    content.append(f"{i}. {option}\n")

        return content

    def set_show_answer(self, show: bool) -> None:
        """Update whether to show answer.

        Args:
            show: Whether to show the answer
        """
        self.show_answer = show
        self.refresh()
