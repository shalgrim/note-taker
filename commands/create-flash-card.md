# Create Flash Card

Create a new flash card and save it to the user's flashcard collection.

## Instructions

1. Ask the user for the following information (or extract from context if they've already provided it):
   - **Question/Prompt**: The front of the card
   - **Answer**: The back of the card
   - **Type**: QA (default), cloze, or multiple_choice
   - **Tags**: Categories/topics for organization (comma-separated)

2. For **cloze** type: The answer should be embedded in the question using `{{answer}}` syntax
   - Example: "The time complexity of binary search is {{O(log n)}}"

3. For **multiple_choice** type: Also ask for:
   - Options (array of choices)
   - Correct answer index(es)

4. Generate a UUID for the card ID

5. Read the existing flashcards from `~/.flashcards/flashcards.json`

6. Add the new card with this structure:
```json
{
  "id": "generated-uuid",
  "type": "qa",
  "question": "user's question",
  "answer": "user's answer",
  "tags": ["tag1", "tag2"],
  "created_at": "ISO-8601 timestamp",
  "last_reviewed": null,
  "next_review": "ISO-8601 timestamp (now, for immediate availability)",
  "ease_factor": 2.5,
  "interval_days": 0,
  "review_count": 0,
  "review_history": []
}
```

7. Write the updated JSON back to `~/.flashcards/flashcards.json`

8. Confirm to the user that the card was created, showing them a preview

## Arguments

$ARGUMENTS - Optional: Can include question, answer, and tags inline. Example: `/create-flash-card "What is O(1)?" "Constant time" tags:algorithms,complexity`
