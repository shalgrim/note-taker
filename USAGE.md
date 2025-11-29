# Flash Card Study - Quick Start Guide

## Installation

Run the setup script to install everything:

```bash
./setup.sh
```

This will:
1. Create `~/.flashcards/` directory and initialize `flashcards.json`
2. Install Claude Code slash commands to `~/.claude/commands/`
3. Install the `flashcard-study` Python package

## Two Ways to Use the System

### 1. Standalone TUI (Token-Free)

Use the `flashcard-study` command for daily reviews without using Claude Code tokens:

```bash
# Launch the interactive TUI
flashcard-study

# Quick stats view
flashcard-study --stats
```

**TUI Features:**
- **Home Dashboard**: View statistics at a glance
- **Quiz Mode**: Review cards with spaced repetition
- **Card Management**: Create, edit, delete cards
- **Statistics**: Detailed breakdown of your progress

**Keyboard Shortcuts:**
- `s` - Start quiz
- `l` - Browse card list
- `n` - Create new card
- `t` - View statistics
- `q` - Quit
- `Space` - Reveal answer (during quiz)
- `0` - Score wrong (during quiz)
- `5` - Score partial (during quiz)
- `1` - Score correct (during quiz)
- `Esc` - Go back / Cancel

### 2. Claude Code Integration (AI-Assisted)

Use Claude Code slash commands for AI-assisted card creation and learning:

```bash
# Create a card with Claude's help
/create-flash-card

# Review cards with Claude
/quiz
/quiz tags:algorithms
/quiz count:5
/quiz all

# Extract cards from a learning conversation
/capture-notes
/capture-notes tags:python,web
```

## Example Workflow

### Daily Review (Token-Free)

```bash
# Morning: Check what's due
flashcard-study --stats

# Review due cards
flashcard-study
# Press 's' to start quiz
# Follow prompts, score yourself
```

### Learning Session (With Claude)

1. Have a conversation with Claude Code about a topic
2. At the end, run `/capture-notes` to extract key learnings
3. Claude suggests potential flash cards
4. Select which to save

### Manual Card Creation

**In the TUI:**
```bash
flashcard-study
# Press 'n' for new card
# Fill in question, answer, type, tags
# Save
```

**With Claude:**
```
/create-flash-card
```
Claude will prompt you for details.

## Card Types

### Question & Answer (QA)
Simple front/back cards.

**Example:**
- Question: "What is the time complexity of bubble sort?"
- Answer: "O(n²) in worst and average case"

### Cloze Deletion
Fill-in-the-blank cards. Use `{{answer}}` syntax.

**Example:**
- Question: "Python uses {{duck typing}} for its type system"
- Answer: "duck typing"

### Multiple Choice
Question with options (manual creation only).

**Example:**
- Question: "Which sorting algorithm has O(n log n) average time?"
- Options: ["Bubble Sort", "Merge Sort", "Selection Sort", "Insertion Sort"]
- Answer: "Merge Sort"

## Spaced Repetition Scoring

When reviewing cards, score yourself honestly:

- **0** (Wrong): Didn't know the answer → Reset to 1 day
- **0.5** (Partial): Knew part of it → Moderate increase
- **1** (Correct): Knew it fully → Interval increases by ease factor

The algorithm automatically adjusts:
- Cards you know well: Appear less frequently
- Cards you struggle with: Appear more frequently
- New cards: Appear frequently until mastered

## Tips

1. **Be honest with scoring**: The algorithm only works if you're truthful
2. **Review daily**: Even 5-10 cards/day builds long-term retention
3. **Use tags**: Organize by topic, language, difficulty, etc.
4. **Mix modes**: Use TUI for daily reviews, Claude for creating quality cards
5. **Keep answers concise**: Easier to recall and review

## Data Location

All your flash cards are stored in:
```
~/.flashcards/flashcards.json
```

This file is:
- Backed up automatically before each write (`.json.bak`)
- Portable (copy to another machine)
- Plain JSON (can be edited manually if needed)
- Shared between TUI and Claude Code

## Troubleshooting

**TUI won't launch:**
```bash
pip3 install -e /path/to/note-taker
```

**No cards showing:**
```bash
# Check the file exists
ls ~/.flashcards/flashcards.json

# View stats
flashcard-study --stats
```

**Want to reset:**
```bash
# Backup first!
cp ~/.flashcards/flashcards.json ~/.flashcards/backup.json

# Start fresh
echo '{"version": "1.0", "cards": []}' > ~/.flashcards/flashcards.json
```
