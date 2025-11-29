# Note Taker - Flash Card Learning System

A spaced repetition flash card system with both Claude Code integration and a standalone terminal UI for token-free reviews.

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

## Standalone TUI Application

### `flashcard-study`

Launch the interactive terminal UI for token-free flash card management and review.

```bash
flashcard-study           # Launch TUI
flashcard-study --stats   # Quick statistics view
flashcard-study --help    # Show all options
```

**Features:**
- Dashboard with statistics (due today, reviewed, streak, total)
- Quiz mode with progress tracking and keyboard shortcuts
- Browse and manage cards (create, edit, delete)
- Detailed statistics screen
- Full keyboard navigation

**Keyboard Shortcuts:**
- `s` - Start quiz
- `l` - Browse card list
- `n` - Create new card
- `t` - View statistics
- `q` - Quit
- `Space` - Reveal answer (during quiz)
- `0` / `5` / `1` - Score wrong/partial/correct (during quiz)

### Export to Anki

Export your cards to Anki format (.apkg files) for use in Anki desktop or mobile apps.

```bash
flashcard-study export cards.apkg                           # Export all to "Claude Code" deck
flashcard-study export --deck "Python" cards.apkg          # Custom deck name
flashcard-study export --tags algorithms cards.apkg        # Filter by tags
flashcard-study export --deck "Web" --tags react web.apkg  # Combined
```

All cards are exported with their tags preserved. Supports QA, cloze, and multiple choice card types.

## Claude Code Commands

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
