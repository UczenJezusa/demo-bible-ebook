from utils.verse_accessor import VerseAccessor
from utils.formatter_wrapper import FormatterWrapper
from utils.verse_dispatcher import VerseDispatcher
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ProcessingCoordinator:
    """
    Koordynator przetwarzania wersetów.
    Ogólny stos wywołań: ProcessingCoordinator -> VerseDispatcher -> FormatterWrapper ( -> VerseFormatter -> VerseAccessor )
    """
    def __init__(self, bible_text):
        self.verse_accessor = VerseAccessor(bible_text)
        self.formatter = FormatterWrapper()
        self.verse_dispatcher = VerseDispatcher(self.verse_accessor, self.formatter)

    def process_all(self):
        i = 0
        while i < len(self.verse_accessor.bible_text):
            verse = self.verse_accessor.bible_text[i]

            # 1) Aktualizacja flag ksiąg
            self.verse_dispatcher.update_book_flags(verse)

            # 2) Pierwsze wersety psalmu
            psalm_header = self.verse_dispatcher.is_psalm_header(verse)
            if psalm_header:
                self.verse_dispatcher.dispatch_psalm(i, psalm_header)
                i += 1
                continue

            # 3) Pierwsze wersety pozostałych ksiąg
            roman_header = self.verse_dispatcher.extract_roman_number_from_header(verse)
            if roman_header:
                self.verse_dispatcher.dispatch_chapter(i, verse, roman_header)
                i += 1
                continue

            # 4) wersety nie wymagające formatowania
            i += 1

    def save_back(self, filename: Path) -> None:
        if self.verse_accessor.changes_made > 0:
            filename.write_text(''.join(self.verse_accessor.bible_text), encoding='utf-8')
            logger.info('Successfully modified %s file', filename)
        else:
            logger.info("File %s was not modified. No verses requiring formatting were found.", filename)
