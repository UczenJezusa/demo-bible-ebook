import re
from typing import Tuple
from utils.formatter import VerseFormatter

class PsalmSet1Formatter:
    @staticmethod
    def format(parsed_verse: Tuple[str, str, str], fmt: VerseFormatter) -> str:
        verse_number, first_sent, rest = parsed_verse
        if rest.lstrip():
            return fmt.format_verse(
                '',
                f'{verse_number or ""}{first_sent}<br>{fmt.make_first_letter_span(rest.lstrip()[0])}{rest.lstrip()[1:]}'
            )
        return fmt.format_verse('', f'{verse_number or ""}{first_sent}')

class PrzypSet1Formatter:
    @staticmethod
    def format(parsed_verse: Tuple[str, str, str], fmt: VerseFormatter) -> str:
        _, first_sent, rest = parsed_verse
        if rest.lstrip():
            return fmt.format_verse(
                '',
                f'{first_sent}<br>{fmt.make_first_letter_span(rest.lstrip()[0])}{rest.lstrip()[1:]}'
            )
        return fmt.format_verse('', first_sent)

class TrenyFormatter:
    @staticmethod
    def format(parsed_verse: Tuple[str, str, str, str], fmt: VerseFormatter) -> str:
        _, first_letter, second_part, remaining_part = parsed_verse
        text = f"{first_letter}{second_part}{remaining_part}"
        text_with_break = fmt.insert_break_after_first_sentence(text)
        text_with_formatted = re.sub(
            r'\s(Ach)',
            r'<br>1. <span style="font-size: 1.9em; margin-right: 0px;">A</span>ch',
            text_with_break,
        )
        return fmt.format_verse('', text_with_formatted)
