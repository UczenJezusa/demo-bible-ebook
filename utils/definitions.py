from typing import Set

# Zbiory dla Psalmów
PSALM_SET_1: Set[str] = {
    'XI', 'XV', 'XVII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXXII', 'XXXV', 'XXXVII',
    'L', 'LXXII', 'LXXIII', 'LXXIV', 'LXXVIII', 'LXXIX', 'LXXXII', 'LXXXVI', 'LXXXVII', 'XC', 'XCVIII',
    'C', 'CI', 'CIII', 'CVI', 'CIX', 'CX', 'CXI', 'CXII', 'CXIII', 'CXX', 'CXXI', 'CXXII', 'CXXIII', 'CXXIV',
    'CXXV', 'CXXVI', 'CXXVII', 'CXXVIII', 'CXXIX', 'CXXX', 'CXXXI', 'CXXXII', 'CXXXIII', 'CXXXIV',
    'CXXXV', 'CXXXVIII', 'CXXXIX', 'CXLI', 'CXLIII', 'CXLIV', 'CXLV', 'CXLVIII', 'CXLIX', 'CL'
}
PSALM_SET_2: Set[str] = {
    'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'XII', 'XIII', 'XIV', 'XVI', 'XVIII', 'XIX', 'XX', 'XXI',
    'XXII', 'XXX', 'XXXI', 'XXXIV', 'XXXVI', 'XXXVIII', 'XXXIX', 'XL', 'XLI', 'XLII', 'XLIV', 'XLV', 'XLVI',
    'XLVII', 'XLVIII', 'XLIX', 'LIII', 'LV', 'LVI', 'LVII', 'LVIII', 'LIX', 'LXI', 'LXII', 'LXIII', 'LXIV',
    'LXV', 'LXVI', 'LXVII', 'LXVIII', 'LXIX', 'LXX', 'LXXV', 'LXXVI', 'LXXVII', 'LXXX', 'LXXXI', 'LXXXIII',
    'LXXXIV', 'LXXXV', 'LXXXVIII', 'LXXXIX', 'XCII', 'CII', 'CVIII', 'CXL', 'CXLII', 'CXLVI'
}
PSALM_SET_3: Set[str] = {'LI', 'LII', 'LIV', 'LX'}

# Lista psalmów ze zwykłym formatowaniem pierwszego wersetu:
# 1-2, 10, 33, 43, 71, 91, 93-97, 99, 104 - 105, 107, 114, 115-119, 136-137, 147

# Zbiory dla Przypowieści, Pieśni i Abakuka
PRZYP_SET_1: Set[str] = {'X'}
PRZYP_SET_2: Set[str] = {'XXV', 'XXX', 'XXXI'}
PIESN_SET_2: Set[str] = {'I'}
ABAKUK_SET_2: Set[str] = {'III'}

FIRST_LETTER_SPAN_TEMPLATE = '<span style="font-size: 1.9em; margin-right: {margin};">{char}</span>'

MARGIN_MAP = {
    'W': '-3.2px', 'P': '-2.5px', 'N': '-1.9px', 'U': '-2.1px',
    'B': '-1.5px', 'G': '-1.5px', 'D': '-1px',
}

# Numer wersetu ulegający formatowaniu
PSALM_OFFSET_SET1 = 1
PSALM_OFFSET_SET2 = 2
PSALM_OFFSET_SET3 = 3

NUM_OF_SPECIAL_FORMAT_FOR_PRZYP = 4
