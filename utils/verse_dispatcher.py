import re
from enum import Enum, auto
from typing import List, Set, Tuple, Optional
from utils.formatter_wrapper import FormatterWrapper
from utils.verse_accessor import VerseAccessor
from utils.special_handlers import PsalmSet1Formatter, PrzypSet1Formatter, TrenyFormatter
from utils.definitions import *

class BookFlag(Enum):
    PRZYP = auto()
    PIESN = auto()
    TRENY = auto()
    ABAKUK = auto()

class VerseDispatcher:
    """Delegowanie do odpowiednich funkcji formatujących."""

    PATTERN_PSALM_HEADER = re.compile(
        r'(?i)<p[^>]*>\s*<span[^>]*>\s*<span[^>]*>(P)</span>(SALM)</span>\s*'
        r'<span[^>]*>([IVXLCDM]+)</span>\s*<span[^>]*>\.</span>\s*</p>'
    )
    PATTERN_CHAPTER_HEADER = re.compile(
            r'(?i)<p[^>]*>\s*<span[^>]*>\s*<span[^>]*>[A-Z]</span>[A-Z]+</span>\s*'
            r'<span[^>]*>\s*([MDCLXVI]+)\s*</span>\s*<span[^>]*>\s*\.\s*</span>\s*</p>'
        )
    PATTERN_PRZYP_BOOK_HEADER = re.compile(r'ci Salomonowych')
    PATTERN_PIESN_BOOK_HEADER = re.compile(r'niami Salomonowa')
    PATTERN_TRENY_BOOK_HEADER = re.compile(r'Narzekania Jeremijaszowe')
    PATTERN_ABAKUK_BOOK_HEADER = re.compile(r'bakukowe')

    def __init__(self, verse_accessor: VerseAccessor, formatter: FormatterWrapper):
        self.verse_accessor = verse_accessor
        self.formatter = formatter
        self.book_flags: Set[BookFlag] = set()
        self.przyp_counter: int = 0

        self.psalm_handler_map: List[Tuple[Set[str], int, callable]] = [
            (PSALM_SET_1, PSALM_OFFSET_SET1, self._psalm_set1_handler),
            (PSALM_SET_2, PSALM_OFFSET_SET2, self._psalm_set2_or_set3_handler),
            (PSALM_SET_3, PSALM_OFFSET_SET3, self._psalm_set2_or_set3_handler),
        ]

    # ----- aktualizacja flag ksiąg -----
    def update_book_flags(self, verse: str) -> None:
        if self.PATTERN_PRZYP_BOOK_HEADER.search(verse):
            self.book_flags.add(BookFlag.PRZYP)
        if self.PATTERN_PIESN_BOOK_HEADER.search(verse):
            self.book_flags.add(BookFlag.PIESN)
        if self.PATTERN_TRENY_BOOK_HEADER.search(verse):
            self.book_flags.add(BookFlag.TRENY)
        if self.PATTERN_ABAKUK_BOOK_HEADER.search(verse):
            self.book_flags.add(BookFlag.ABAKUK)

    # ----- rozpoznawanie nagłówków rozdziałów/psalmów -----
    def is_psalm_header(self, verse: str) -> Optional[re.Match]:
        return self.PATTERN_PSALM_HEADER.search(verse)
    
    def extract_roman_number_from_header(self, verse: str) -> Optional[str]:
        # specyficzny wzorzec wersetu
        roman_number_match = self.PATTERN_CHAPTER_HEADER.search(verse)
        if roman_number_match:
            return (roman_number_match.group(1) or '').strip().upper()
        # ogólny wzorzec wersetu 
        text = re.sub(r'<[^>]+>', '', verse)
        roman_number_match = re.search(r'\b([MDCLXVI]+)\.?\b', text, flags=re.IGNORECASE)
        return (roman_number_match.group(1) or '').upper() if roman_number_match else None

    # ----- handler-y psalmów -----
    def _psalm_set1_handler(self, idx: int) -> bool:
        return self.formatter.handle_special_format_verse(idx, self.verse_accessor, self.formatter.formatter.parse_split_first_verse, PsalmSet1Formatter.format)

    def _psalm_set2_or_set3_handler(self, idx: int) -> bool:
        return self.formatter.handle_normal_format_verse(idx, self.verse_accessor, keep_number=True)
    
    # ----- funkcje wybierające odpowiedni sposób formatowania wersetu -----
    def dispatch_psalm(self, idx: int, psalm_header: re.Match) -> None:
        """Wybiera odpowiedni sposób formatowania wersetu psalmu."""
        psalm_number = psalm_header.group(3).strip().upper() if psalm_header else None
        if not psalm_number:
            return

        # psalmy należące do psalm_set1, 2 i 3:
        psalm_set_handled = False
        for psalm_set, offset, handler in self.psalm_handler_map:
            if psalm_number in psalm_set:
                idx2 = idx + offset
                if self.verse_accessor.is_valid_verse_number(idx2):
                    handler(idx2)
                psalm_set_handled = True
                break

        # pozostałe psalmy:
        if not psalm_set_handled:
            idx2 = idx + 1
            if self.verse_accessor.is_valid_verse_number(idx2):
                self.formatter.handle_normal_format_verse(idx2, self.verse_accessor)

    def dispatch_chapter(self, i: int, verse: str, roman_header: str) -> None:
        """Wybiera odpowiedni sposób formatowania wersetu rozdziału."""
        if BookFlag.PRZYP in self.book_flags and roman_header in (PRZYP_SET_1.union(PRZYP_SET_2)):
            self.przyp_counter += 1
            if self.przyp_counter >= NUM_OF_SPECIAL_FORMAT_FOR_PRZYP:
                self.book_flags.discard(BookFlag.PRZYP)
            if roman_header in PRZYP_SET_1:
                idx2 = i + 1
                if self.verse_accessor.is_valid_verse_number(idx2):
                    self.formatter.handle_special_format_verse(idx2, self.verse_accessor, self.formatter.formatter.parse_split_first_verse, PrzypSet1Formatter.format)
            elif roman_header in PRZYP_SET_2:
                idx2 = i + 2
                if self.verse_accessor.is_valid_verse_number(idx2):
                    self.formatter.handle_normal_format_verse(idx2, self.verse_accessor, True)
            return

        if BookFlag.PIESN in self.book_flags and roman_header in PIESN_SET_2:
            idx2 = i + 2
            if self.verse_accessor.is_valid_verse_number(idx2):
                self.formatter.handle_normal_format_verse(idx2, self.verse_accessor, True)
            self.book_flags.discard(BookFlag.PIESN)
            return

        if BookFlag.TRENY in self.book_flags:
            self.book_flags.discard(BookFlag.TRENY)
            idx2 = i + 1
            if self.verse_accessor.is_valid_verse_number(idx2):
                self.formatter.handle_special_format_verse(idx2, self.verse_accessor, self.formatter.formatter.parse_verse, TrenyFormatter.format)
            return

        if BookFlag.ABAKUK in self.book_flags and roman_header in ABAKUK_SET_2:
            idx2 = i + 2
            if self.verse_accessor.is_valid_verse_number(idx2):
                self.formatter.handle_normal_format_verse(idx2, self.verse_accessor, True)
            self.book_flags.discard(BookFlag.ABAKUK)
            return

        # reszta rozdziałów - formatowanie zwykłe
        if '<br><p' in verse:
            idx2 = i + 1
            if self.verse_accessor.is_valid_verse_number(idx2):
                self.formatter.handle_normal_format_verse(idx2, self.verse_accessor)
