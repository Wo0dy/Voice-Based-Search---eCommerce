"""
Load the input file (see https://fasttext.cc/docs/en/english-vectors.html)
and do some cleanup.
"""

from typing import Iterable, List, Set

import re
import vectors as v
from word import Word


def load_words(file_path: str) -> List[Word]:
    """Load and cleanup the data."""
    print(f"Loading {file_path}...")
    words = load_words_raw(file_path)
    print(f"Loaded {len(words)} words.")

    words = [w for w in words if len(w.vector) == 300]

    words = remove_stop_words(words)
    print(f"Removed stop words, {len(words)} remain.")

    words = remove_duplicates(words)
    print(f"Removed duplicates, {len(words)} remain.")

    return words


def load_words_raw(file_path: str) -> List[Word]:
    """Load the file as-is, without doing any validation or cleanup."""

    def parse_line(line: str, frequency: int) -> Word:
        tokens = line.split()
        word = tokens[0]
        vector = v.normalize([float(x) for x in tokens[1:]])
        return Word(word, vector, frequency)

    words = []
    # Words are sorted from the most common to the least common ones
    frequency = 1
    with open(file_path, encoding='utf8') as f:
        for line in f:
            w = parse_line(line, frequency)
            words.append(w)
            frequency += 1
    return words


def iter_len(iter: Iterable[complex]) -> int:
    return sum(1 for _ in iter)


# We want to ignore these characters,
# so that e.g. "U.S.", "U.S", "US_" and "US" are the same word.
ignore_char_regex = re.compile("[\W_]")

# Has to start and end with an alphanumeric character
is_valid_word = re.compile("^[^\W_].*[^\W_]$")


def remove_duplicates(words: List[Word]) -> List[Word]:
    seen_words: Set[str] = set()
    unique_words: List[Word] = []
    for w in words:
        canonical = ignore_char_regex.sub("", w.text)
        if not canonical in seen_words:
            seen_words.add(canonical)
            # Keep the original ordering
            unique_words.append(w)
    return unique_words


def remove_stop_words(words: List[Word]) -> List[Word]:
    return [w for w in words if (
            len(w.text) > 1 and is_valid_word.match(w.text))]


# Run "smoke tests" on import
assert [w.text for w in remove_stop_words([
    Word('a', [], 1),
    Word('ab', [], 1),
    Word('-ab', [], 1),
    Word('ab_', [], 1),
    Word('a.', [], 1),
    Word('.a', [], 1),
    Word('ab', [], 1),
])] == ['ab', 'ab']
assert [w.text for w in remove_duplicates([
    Word('a.b', [], 1),
    Word('-a-b', [], 1),
    Word('ab_+', [], 1),
    Word('.abc...', [], 1),
])] == ['a.b', '.abc...']
