import re
from utils.formatter import VerseFormatter
from utils.verse_accessor import VerseAccessor
from typing import Optional, Callable

ParserFn = Callable[[str], Optional[tuple]]
StatelessSpecialFormatterFn = Callable[[tuple, VerseFormatter], str]

class FormatterWrapper:
    """Wrapper (zewnętrzny interfejs, funkcje wyższego poziomu) dla VerseFormatter + dodatkowe helpery."""
    def __init__(self):
        self.formatter = VerseFormatter()

    def handle_special_format_verse(
        self,
        idx: int,
        verse_accessor: VerseAccessor,
        parser: ParserFn, # struktura wersetu
        special_formatter: StatelessSpecialFormatterFn
    ) -> bool:
        verse = verse_accessor.get_verse(idx)
        if not verse:
            return False
        parsed_verse = parser(verse)
        if not parsed_verse:
            return False
        new_html = special_formatter(parsed_verse, self.formatter)
        return verse_accessor.modify_verse(idx, new_html)

    def handle_normal_format_verse(self, idx: int, verse_accessor: VerseAccessor, keep_number: bool = False) -> bool:
        verse = verse_accessor.get_verse(idx)
        if not verse:
            return False

        parsed_verse = self.formatter.parse_verse(verse)
        verse_number = f"{parsed_verse[0]} " if (parsed_verse and keep_number) else ""  

        verse_match = self.formatter.match_verse(verse)
        if not verse_match:
            if not parsed_verse:
                return False
            _, first_letter, second_part, remaining_part = parsed_verse
            span = self.formatter.make_first_letter_span(first_letter)
            new_inner = f'{span}{second_part}{remaining_part}'
            return verse_accessor.modify_verse(idx, self.formatter.format_verse(verse_number, new_inner))

        inner_html = verse_match.group(1) or ''
        
        # obsługuje również przypadek w którym pierwszy wyraz wersetu jest otagowany kursywą - opcjonalne wystąpienie "<i>" w wersecie
        match = re.match(r'^(<i>)?([^\W\d_])([^<]*)(.*)$', inner_html, flags=re.UNICODE | re.DOTALL)
        if not match:
            return False
        is_italic, first_letter, second_part, rest = match.group(1) or '', (match.group(2) or '').upper(), match.group(3) or '', match.group(4) or ''
        close_tag = '</i>' if is_italic and not rest.lstrip().startswith('</i>') else ''
        inner = f'{is_italic}{self.formatter.make_first_letter_span(first_letter)}{second_part}{close_tag}{rest}'
        return verse_accessor.modify_verse(idx, self.formatter.format_verse(verse_number, inner))
