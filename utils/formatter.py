import re
from typing import Optional, Tuple
from utils.definitions import FIRST_LETTER_SPAN_TEMPLATE, MARGIN_MAP

def get_margin_right(letter: str) -> str:
    """Zwraca margines dla podanej litery."""
    if not letter:
        return '0px'
    return MARGIN_MAP.get(letter.upper(), '0px')

class VerseFormatter:
    """Helper do parsowania i budowania/tworzenia nowych wersetów w HTML."""

    PARSE_VERSE_RE = re.compile(r'<p[^>]*>\s*(\d+\.)?\s*([^\W\d_])([^<]*)(.*)</p>', re.UNICODE)
    PARSE_SPLIT_FIRST_VERSE_RE = re.compile(
        r'^<p[^>]*>\s*(\d+\.\s*)?(.*?[\.\?\!])\s*(.+)</p>\s*$', re.UNICODE | re.DOTALL
    )
    MATCH_VERSE_RE = re.compile(r'<p[^>]*>\s*1\.\s*(.*)</p>', re.UNICODE | re.DOTALL)
    
    def match_verse(self, verse: str) -> Optional[re.Match]:
        return self.MATCH_VERSE_RE.search(verse)
    
    # Zwraca strukturę wersetu
    def parse_verse(self, verse: str) -> Optional[Tuple[str, str, str, str]]:
        match = self.PARSE_VERSE_RE.search(verse)
        if not match:
            return None
        return (match.group(1) or '', (match.group(2) or '').upper(), match.group(3) or '', match.group(4) or '')

    # Zwraca strukturę wersetu do przetworzenia dla Psalm_set1 i Przyp_set1
    # split = użycie `<br>`
    def parse_split_first_verse(self, verse: str) -> Optional[Tuple[str, str, str]]:
        match = self.PARSE_SPLIT_FIRST_VERSE_RE.match(verse)
        if not match:
            return None
        return (match.group(1) or '', match.group(2) or '', match.group(3) or '')

    def make_first_letter_span(self, ch: str) -> str:
        return FIRST_LETTER_SPAN_TEMPLATE.format(margin=get_margin_right(ch), char=(ch or '').upper())

    def format_verse(self, verse_number: str, inner: str, suffix: str = '', add_break: bool = False) -> str:
        if add_break:
            inner = f"{inner}<br>"
        return f'<p class="calibre1">{verse_number}{inner}{suffix}</p>\n'

    def insert_break_after_first_sentence(self, text: str) -> str:
        return re.sub(r'(^[^.?!]*[.?!])\s*', r'\1<br>', text, count=1)

