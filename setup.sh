#!/bin/bash

# Flash Card System Setup Script
# Installs the spaced repetition flash card system for Claude Code

set -e

echo "Setting up Flash Card System..."

# Create directories
mkdir -p ~/.flashcards
mkdir -p ~/.claude/commands

# Initialize flashcards database if it doesn't exist
if [ ! -f ~/.flashcards/flashcards.json ]; then
    cat > ~/.flashcards/flashcards.json << 'EOF'
{
  "version": "1.0",
  "cards": []
}
EOF
    echo "✓ Created ~/.flashcards/flashcards.json"
else
    echo "• ~/.flashcards/flashcards.json already exists, skipping"
fi

# Copy command files
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$SCRIPT_DIR/commands" ]; then
    cp "$SCRIPT_DIR/commands/"*.md ~/.claude/commands/
    echo "✓ Installed slash commands to ~/.claude/commands/"
else
    echo "⚠ No commands directory found. Please copy command files manually."
fi

# Install Python package
echo ""
echo "Installing flashcard-study TUI application..."
if command -v pip3 &> /dev/null; then
    pip3 install -e "$SCRIPT_DIR"
    echo "✓ Installed flashcard-study command"
else
    echo "⚠ pip3 not found. Please install Python 3.11+ and pip3"
    echo "  Then run: pip3 install -e $SCRIPT_DIR"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Claude Code Commands (within Claude):"
echo "  /create-flash-card  - Create a new flash card"
echo "  /quiz               - Review cards with spaced repetition"
echo "  /capture-notes      - Extract cards from conversation"
echo ""
echo "Standalone TUI Application (terminal):"
echo "  flashcard-study           - Launch interactive TUI"
echo "  flashcard-study --help    - Show all options"
echo "  flashcard-study --stats   - Quick statistics view"
