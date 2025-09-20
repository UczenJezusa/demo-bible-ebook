from typing import List, Optional, Set

class VerseAccessor:
    """Zarządza dostępem do wersetów, indeksami przetworzonych wersetów oraz modyfikuje wersety."""

    def __init__(self, bible_text: List[str]):
        self.bible_text = bible_text
        self.processed_verses: Set[int] = set()
        self.changes_made: int = 0

    def is_valid_verse_number(self, idx: int) -> bool:
        return 0 <= idx < len(self.bible_text) and idx not in self.processed_verses

    def get_verse(self, idx: int) -> Optional[str]:
        return self.bible_text[idx] if self.is_valid_verse_number(idx) else None

    def modify_verse(self, idx: int, new_verse: str) -> bool:
        if not self.is_valid_verse_number(idx):
            return False
        self.bible_text[idx] = new_verse
        self.processed_verses.add(idx)
        self.changes_made += 1
        return True
