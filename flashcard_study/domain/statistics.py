"""Statistics calculation for flash cards."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
from ..data.models import FlashCard


@dataclass
class Statistics:
    """Aggregated statistics about flash card usage."""
    total_cards: int
    cards_due_today: int
    cards_due_this_week: int
    cards_reviewed_today: int
    review_streak_days: int
    average_ease_factor: float
    mastery_distribution: dict[str, int]  # "new", "learning", "mastered"
    tag_distribution: dict[str, int]


class StatisticsCalculator:
    """Calculates statistics from flash card data."""

    @staticmethod
    def calculate(cards: list[FlashCard], now: datetime) -> Statistics:
        """Calculate comprehensive statistics.

        Args:
            cards: List of all flash cards
            now: Current time

        Returns:
            Statistics object with all calculated metrics
        """
        total = len(cards)

        if total == 0:
            return Statistics(
                total_cards=0,
                cards_due_today=0,
                cards_due_this_week=0,
                cards_reviewed_today=0,
                review_streak_days=0,
                average_ease_factor=2.5,
                mastery_distribution={"new": 0, "learning": 0, "mastered": 0},
                tag_distribution={}
            )

        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = today_start + timedelta(days=7)

        # Count cards by due date
        due_today = sum(1 for c in cards if c.next_review <= now)
        due_week = sum(1 for c in cards if c.next_review <= week_end)

        # Count cards reviewed today
        reviewed_today = sum(
            1 for c in cards
            if c.last_reviewed and c.last_reviewed >= today_start
        )

        # Mastery distribution
        mastery = {"new": 0, "learning": 0, "mastered": 0}
        for card in cards:
            if card.review_count == 0:
                mastery["new"] += 1
            elif card.review_count < 10:
                mastery["learning"] += 1
            else:
                mastery["mastered"] += 1

        # Tag distribution
        tag_counts = defaultdict(int)
        for card in cards:
            for tag in card.tags:
                tag_counts[tag] += 1

        # Average ease factor
        avg_ease = sum(c.ease_factor for c in cards) / total

        # Streak calculation
        streak = StatisticsCalculator._calculate_streak(cards, now)

        return Statistics(
            total_cards=total,
            cards_due_today=due_today,
            cards_due_this_week=due_week,
            cards_reviewed_today=reviewed_today,
            review_streak_days=streak,
            average_ease_factor=avg_ease,
            mastery_distribution=mastery,
            tag_distribution=dict(tag_counts)
        )

    @staticmethod
    def _calculate_streak(cards: list[FlashCard], now: datetime) -> int:
        """Calculate consecutive days with reviews.

        Args:
            cards: List of all flash cards
            now: Current time

        Returns:
            Number of consecutive days with at least one review
        """
        if not cards:
            return 0

        # Get all review dates
        review_dates = set()
        for card in cards:
            for history in card.review_history:
                review_date = history.date.date()
                review_dates.add(review_date)

        if not review_dates:
            return 0

        # Count consecutive days backwards from today
        streak = 0
        current_date = now.date()

        while current_date in review_dates:
            streak += 1
            current_date -= timedelta(days=1)

        return streak
