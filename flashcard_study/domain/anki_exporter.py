"""Export flash cards to Anki format."""

import genanki
import random
from pathlib import Path
from typing import Optional

from ..data.models import FlashCard


class AnkiExporter:
    """Exports flash cards to Anki .apkg format."""

    # Model IDs - using random but consistent IDs
    QA_MODEL_ID = 1607392319
    CLOZE_MODEL_ID = 1607392320
    MC_MODEL_ID = 1607392321

    def __init__(self, deck_name: str = "Claude Code"):
        """Initialize exporter with deck name.

        Args:
            deck_name: Name of the Anki deck to create
        """
        self.deck_name = deck_name
        # Generate consistent deck ID from name
        self.deck_id = random.randrange(1 << 30, 1 << 31)

    def export(
        self,
        cards: list[FlashCard],
        output_path: Path,
        tags_filter: Optional[list[str]] = None
    ) -> int:
        """Export cards to Anki .apkg file.

        Args:
            cards: List of flash cards to export
            output_path: Path to save .apkg file
            tags_filter: Optional list of tags to filter by (OR logic)

        Returns:
            Number of cards exported
        """
        # Filter by tags if specified
        if tags_filter:
            cards = [c for c in cards if any(t in c.tags for t in tags_filter)]

        if not cards:
            return 0

        # Create Anki deck
        deck = genanki.Deck(self.deck_id, self.deck_name)

        # Create note models
        qa_model = self._create_qa_model()
        cloze_model = self._create_cloze_model()
        mc_model = self._create_mc_model()

        # Add cards to deck
        for card in cards:
            if card.type == "qa":
                note = self._create_qa_note(card, qa_model)
            elif card.type == "cloze":
                note = self._create_cloze_note(card, cloze_model)
            else:  # multiple_choice
                note = self._create_mc_note(card, mc_model)

            deck.add_note(note)

        # Create package and write
        package = genanki.Package(deck)
        package.write_to_file(str(output_path))

        return len(cards)

    def _create_qa_model(self) -> genanki.Model:
        """Create Anki model for Q&A cards."""
        return genanki.Model(
            self.QA_MODEL_ID,
            'Claude Code - Basic',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '<div class="question">{{Question}}</div>',
                    'afmt': '{{FrontSide}}<hr id="answer"><div class="answer">{{Answer}}</div>',
                },
            ],
            css='''
                .card {
                    font-family: arial;
                    font-size: 20px;
                    text-align: center;
                    color: black;
                    background-color: white;
                }
                .question {
                    color: #8be9fd;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                .answer {
                    color: #50fa7b;
                }
            '''
        )

    def _create_cloze_model(self) -> genanki.Model:
        """Create Anki model for cloze deletion cards."""
        return genanki.Model(
            self.CLOZE_MODEL_ID,
            'Claude Code - Cloze',
            fields=[
                {'name': 'Text'},
            ],
            templates=[
                {
                    'name': 'Cloze',
                    'qfmt': '{{cloze:Text}}',
                    'afmt': '{{cloze:Text}}',
                },
            ],
            model_type=genanki.Model.CLOZE,
            css='''
                .card {
                    font-family: arial;
                    font-size: 20px;
                    text-align: center;
                    color: black;
                    background-color: white;
                }
                .cloze {
                    font-weight: bold;
                    color: #8be9fd;
                }
            '''
        )

    def _create_mc_model(self) -> genanki.Model:
        """Create Anki model for multiple choice cards."""
        return genanki.Model(
            self.MC_MODEL_ID,
            'Claude Code - Multiple Choice',
            fields=[
                {'name': 'Question'},
                {'name': 'Options'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '''
                        <div class="question">{{Question}}</div>
                        <div class="options">{{Options}}</div>
                    ''',
                    'afmt': '''
                        {{FrontSide}}
                        <hr id="answer">
                        <div class="answer">{{Answer}}</div>
                    ''',
                },
            ],
            css='''
                .card {
                    font-family: arial;
                    font-size: 20px;
                    text-align: center;
                    color: black;
                    background-color: white;
                }
                .question {
                    color: #8be9fd;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                .options {
                    text-align: left;
                    display: inline-block;
                    margin: 20px 0;
                }
                .answer {
                    color: #50fa7b;
                    font-weight: bold;
                }
            '''
        )

    def _create_qa_note(self, card: FlashCard, model: genanki.Model) -> genanki.Note:
        """Create Anki note for Q&A card."""
        return genanki.Note(
            model=model,
            fields=[card.question, card.answer],
            tags=card.tags,
            guid=str(card.id)  # Use our UUID as GUID for uniqueness
        )

    def _create_cloze_note(self, card: FlashCard, model: genanki.Model) -> genanki.Note:
        """Create Anki note for cloze card."""
        # Convert our {{answer}} format to Anki's {{c1::answer}} format
        import re
        text = re.sub(r'\{\{(.+?)\}\}', r'{{c1::\1}}', card.question)

        return genanki.Note(
            model=model,
            fields=[text],
            tags=card.tags,
            guid=str(card.id)
        )

    def _create_mc_note(self, card: FlashCard, model: genanki.Model) -> genanki.Note:
        """Create Anki note for multiple choice card."""
        # Format options as numbered list
        options_html = "<br>".join([
            f"{i}. {opt}"
            for i, opt in enumerate(card.options or [], 1)
        ])

        return genanki.Note(
            model=model,
            fields=[card.question, options_html, card.answer],
            tags=card.tags,
            guid=str(card.id)
        )
