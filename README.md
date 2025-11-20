# Note Taker - Flash Card Learning System

A spaced repetition flash card system for Claude Code that helps you capture and review learnings from your coding sessions.

## Setup

The system uses global directories so it works from any project:

```
~/.flashcards/flashcards.json    # Card database
~/.claude/commands/              # Slash commands
```

Run the setup script to install:
```bash
./setup.sh
```

## Commands

### `/create-flash-card`
Manually create a new flash card.

```
/create-flash-card
```

You'll be prompted for:
- Question/prompt
- Answer
- Type (QA, cloze, multiple_choice)
- Tags

### `/quiz`
Review cards using spaced repetition.

```
/quiz                      # Review due cards
/quiz tags:algorithms      # Filter by tag
/quiz count:5              # Limit to 5 cards
/quiz all                  # Include cards not yet due
```

### `/capture-notes`
Extract flash cards from the current conversation.

```
/capture-notes
/capture-notes tags:python,web
```

## Card Types

- **QA**: Standard question and answer
- **Cloze**: Fill-in-the-blank using `{{answer}}` syntax
- **Multiple Choice**: Question with options

## Spaced Repetition

Cards are scheduled based on your performance:
- Score `1` (correct): Interval increases
- Score `0.5` (partial): Smaller increase
- Score `0` (incorrect): Reset to 1 day

New cards appear frequently; mastered cards appear less often.

## Inspiration

See [socratic_fp_learning.md](./socratic_fp_learning.md) for the Socratic teaching approach that inspired this system.
