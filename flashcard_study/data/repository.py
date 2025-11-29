"""JSON repository for flash card persistence."""

from pathlib import Path
import json
import shutil
from typing import Optional
from uuid import UUID

from .models import FlashCardDatabase, FlashCard


class FlashCardRepository:
    """Manages persistence of flash cards to JSON file."""

    def __init__(self, file_path: Optional[Path] = None):
        """Initialize repository with file path.

        Args:
            file_path: Path to JSON file. Defaults to ~/.flashcards/flashcards.json
        """
        if file_path is None:
            file_path = Path.home() / ".flashcards" / "flashcards.json"
        self.file_path = file_path
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Create directory if it doesn't exist."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> FlashCardDatabase:
        """Load and validate database from JSON.

        Returns:
            FlashCardDatabase instance

        Raises:
            ValueError: If JSON is invalid and backup recovery fails
        """
        if not self.file_path.exists():
            return FlashCardDatabase()

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return FlashCardDatabase.model_validate(data)
        except Exception as e:
            # Try to restore from backup
            backup_path = self.file_path.with_suffix('.json.bak')
            if backup_path.exists():
                try:
                    with open(backup_path, 'r') as f:
                        data = json.load(f)
                        return FlashCardDatabase.model_validate(data)
                except Exception:
                    pass

            raise ValueError(f"Failed to load flashcards from {self.file_path}: {e}")

    def save(self, database: FlashCardDatabase) -> None:
        """Save database to JSON with atomic write.

        Args:
            database: FlashCardDatabase to persist
        """
        # Create backup if file exists
        if self.file_path.exists():
            backup_path = self.file_path.with_suffix('.json.bak')
            shutil.copy(self.file_path, backup_path)

        # Atomic write: write to temp, then rename
        temp_path = self.file_path.with_suffix('.json.tmp')
        with open(temp_path, 'w') as f:
            f.write(database.model_dump_json(indent=2))

        temp_path.replace(self.file_path)

    def get_card(self, card_id: UUID) -> Optional[FlashCard]:
        """Get a single card by ID.

        Args:
            card_id: UUID of the card to retrieve

        Returns:
            FlashCard if found, None otherwise
        """
        database = self.load()
        for card in database.cards:
            if card.id == card_id:
                return card
        return None

    def add_card(self, card: FlashCard) -> None:
        """Add a new card to the database.

        Args:
            card: FlashCard to add
        """
        database = self.load()
        database.cards.append(card)
        self.save(database)

    def update_card(self, card: FlashCard) -> None:
        """Update an existing card.

        Args:
            card: FlashCard with updated data
        """
        database = self.load()
        for i, existing_card in enumerate(database.cards):
            if existing_card.id == card.id:
                database.cards[i] = card
                self.save(database)
                return
        raise ValueError(f"Card with id {card.id} not found")

    def delete_card(self, card_id: UUID) -> None:
        """Delete a card by ID.

        Args:
            card_id: UUID of the card to delete
        """
        database = self.load()
        database.cards = [c for c in database.cards if c.id != card_id]
        self.save(database)
