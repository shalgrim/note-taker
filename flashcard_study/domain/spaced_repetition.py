"""Spaced repetition algorithm implementation.

This module implements the exact algorithm specified in the /quiz command.
"""

from datetime import datetime, timedelta
from ..data.models import FlashCard, ReviewHistory


def calculate_next_review(
    card: FlashCard,
    score: float,
    review_time: datetime
) -> tuple[float, float, datetime]:
    """Calculate next review parameters based on score.

    Implements the exact algorithm from /quiz command:
    - score == 0: Reset to 1 day, decrease ease_factor by 0.2
    - score < 1: Scale interval by score * ease_factor, decrease ease_factor by 0.1
    - score == 1: Multiply interval by ease_factor, increase ease_factor by 0.1

    Args:
        card: The flash card being reviewed
        score: Score from 0 to 1 (0 = wrong, 0.5 = partial, 1 = correct)
        review_time: When the review occurred

    Returns:
        Tuple of (interval_days, ease_factor, next_review)
    """
    ease_factor = card.ease_factor
    interval_days = card.interval_days

    if score == 0:
        interval_days = 1
        ease_factor = max(1.3, ease_factor - 0.2)
    elif score < 1:
        interval_days = max(1, interval_days * score * ease_factor)
        ease_factor = max(1.3, ease_factor - 0.1)
    else:  # score == 1
        if interval_days == 0:
            interval_days = 1
        else:
            interval_days = interval_days * ease_factor
        ease_factor = min(3.0, ease_factor + 0.1)

    next_review = review_time + timedelta(days=interval_days)
    return interval_days, ease_factor, next_review


def apply_review(
    card: FlashCard,
    score: float,
    review_time: datetime
) -> FlashCard:
    """Create updated card after review (immutable pattern).

    Args:
        card: The flash card being reviewed
        score: Score from 0 to 1
        review_time: When the review occurred

    Returns:
        New FlashCard instance with updated spaced repetition metadata
    """
    interval_days, ease_factor, next_review = calculate_next_review(
        card, score, review_time
    )

    history_entry = ReviewHistory(
        date=review_time,
        score=score,
        interval_days=interval_days
    )

    return card.model_copy(update={
        "last_reviewed": review_time,
        "next_review": next_review,
        "ease_factor": ease_factor,
        "interval_days": interval_days,
        "review_count": card.review_count + 1,
        "review_history": card.review_history + [history_entry]
    })
