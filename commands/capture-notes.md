# Capture Notes as Flash Cards

Review the current conversation and extract key learnings as flash cards.

## Instructions

1. Analyze the conversation above this command for:
   - Key concepts explained
   - Questions asked and answered
   - "Aha moments" or important realizations
   - Definitions or terminology
   - Examples that illustrate concepts
   - Common mistakes or misconceptions corrected

2. For each potential flash card, create a QA or cloze card:
   - Prefer **cloze** for definitions and fill-in-the-blank facts
   - Prefer **QA** for conceptual questions, "why" questions, and examples

3. Present the extracted cards to the user in a numbered list:
   ```
   Found 3 potential flash cards:

   1. [QA] What is the time complexity of binary search?
      → O(log n)
      Tags: algorithms, complexity

   2. [Cloze] Binary search requires the array to be {{sorted}}
      Tags: algorithms, prerequisites

   3. [QA] Why does binary search have O(log n) complexity?
      → Because it halves the search space with each comparison
      Tags: algorithms, complexity
   ```

4. Ask the user which cards to save:
   - "all" - Save all cards
   - "1,3" - Save specific cards by number
   - "none" - Cancel
   - User can also suggest edits before saving

5. For selected cards, follow the same save process as `/create-flash-card`:
   - Generate UUIDs
   - Add timestamps
   - Initialize spaced repetition fields
   - Save to `~/.flashcards/flashcards.json`

6. Confirm how many cards were saved

## Auto-Suggest Tags

Infer tags from:
- Explicit topics mentioned in conversation
- Technical domains (algorithms, web-dev, databases, etc.)
- Programming languages mentioned
- Concepts (recursion, caching, testing, etc.)

## Arguments

$ARGUMENTS - Optional: Specify tags to apply to all captured cards
- `/capture-notes` - Auto-detect tags
- `/capture-notes tags:algorithms,trees` - Apply these tags to all cards
