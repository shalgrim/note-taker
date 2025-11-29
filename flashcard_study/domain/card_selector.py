"""Card selection logic for quizzes."""

from datetime import datetime
from typing import Optional
from ..data.models import FlashCard


class CardSelector:
    """Selects cards for quiz based on spaced repetition priority."""

    @staticmethod
    def select_for_quiz(
        cards: list[FlashCard],
        tags: Optional[list[str]] = None,
        count: int = 10,
        include_all: bool = False,
        now: Optional[datetime] = None
    ) -> list[FlashCard]:
        """Select cards for quiz based on spaced repetition priority.

        Priority (as per /quiz command):
        1. Overdue cards (most overdue first)
        2. Never reviewed cards (last_reviewed = None)
        3. If include_all: upcoming cards (soonest first)

        Args:
            cards: List of all available cards
            tags: Optional list of tags to filter by (OR logic)
            count: Maximum number of cards to return
            include_all: If True, include cards not yet due
            now: Current time (defaults to datetime.now())

        Returns:
            List of selected cards in priority order
        """
        if now is None:
            now = datetime.now()

        # Filter by tags if specified
        if tags:
            cards = [c for c in cards if any(t in c.tags for t in tags)]

        # Separate into categories
        overdue = []
        never_reviewed = []
        upcoming = []

        for card in cards:
            if card.last_reviewed is None:
                never_reviewed.append(card)
            elif card.next_review <= now:
                # Calculate how overdue (in seconds for sorting)
                overdue_amount = (now - card.next_review).total_seconds()
                overdue.append((card, overdue_amount))
            elif include_all:
                upcoming.append((card, card.next_review))

        # Sort by priority
        overdue.sort(key=lambda x: x[1], reverse=True)  # Most overdue first
        upcoming.sort(key=lambda x: x[1])  # Soonest due first

        # Combine and limit
        result = [c for c, _ in overdue] + never_reviewed + [c for c, _ in upcoming]
        return result[:count]
