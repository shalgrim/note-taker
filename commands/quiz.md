# Quiz Flash Cards

Quiz the user on their flash cards using spaced repetition.

## Instructions

### Setup

1. Read flash cards from `~/.flashcards/flashcards.json`

2. Parse any arguments for filtering:
   - `tags:tag1,tag2` - Only quiz cards with these tags
   - `all` - Include all cards regardless of review schedule
   - `count:N` - Limit to N cards (default: 10)

3. Select cards for review using spaced repetition priority:
   - Cards past their `next_review` date (overdue first, sorted by most overdue)
   - Cards with `next_review` of null (never reviewed)
   - If `all` flag: include cards not yet due, sorted by soonest due

4. If no cards are due, inform the user and show when the next card is due

### Quiz Flow

For each card:

1. Display the question:
   - For **QA**: Show the question
   - For **cloze**: Show the text with `{{...}}` replaced by `_____`
   - For **multiple_choice**: Show question and numbered options

2. Wait for the user to respond with "show answer", "reveal", "s", or similar

3. Display the answer:
   - For **QA**: Show the answer
   - For **cloze**: Show the complete text with the answer highlighted
   - For **multiple_choice**: Show the correct option(s)

4. Ask the user to score themselves:
   - `0` - Incorrect / didn't know
   - `0.5` (or any decimal) - Partial credit
   - `1` - Correct

5. Update the card based on score using spaced repetition:

```
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

next_review = now + interval_days
```

6. Add to review_history:
```json
{
  "date": "ISO-8601 timestamp",
  "score": 0.5,
  "interval_days": 3
}
```

7. Update `last_reviewed`, `next_review`, `review_count`, `ease_factor`, `interval_days`

8. Save to `~/.flashcards/flashcards.json` after each card (in case of interruption)

9. Ask "Next card?" or let user type "done" / "quit" to end session

### End of Session

Show summary:
- Cards reviewed
- Average score
- Cards due tomorrow

## Arguments

$ARGUMENTS - Optional filters. Examples:
- `/quiz` - Review due cards
- `/quiz tags:algorithms` - Only algorithm cards
- `/quiz count:5` - Only 5 cards
- `/quiz all tags:python` - All python cards regardless of schedule
