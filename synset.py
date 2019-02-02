from typing import List, Optional, Tuple
import os
from load import load_words
import vectors as v
from vectors import Vector
from word import Word


def most_similar(base_vector: Vector, words: List[Word]) -> List[Tuple[float, Word]]:
    """Finds n words with smallest cosine similarity to a given word"""
    words_with_distance = [(v.cosine_similarity_normalized(base_vector, w.vector), w) for w in words]
    # We want cosine similarity to be as large as possible (close to 1)
    sorted_by_distance = sorted(words_with_distance, key=lambda t: t[0], reverse=True)
    return sorted_by_distance


def print_most_similar(words: List[Word], text: str) -> None:
    base_word = find_word(text, words)
    if not base_word:
        print(f"Uknown word: {text}")
        return
    #print(f"Words related to {base_word.text}:")
    sorted_by_distance = [
        word.text for (dist, word) in
        most_similar(base_word.vector, words)
        if word.text.lower() != base_word.text.lower()
    ]
    # print(', '.join(sorted_by_distance[:10]))
    return sorted_by_distance[:10]


def read_word() -> str:
    return input("Type a word: ")


def find_word(text: str, words: List[Word]) -> Optional[Word]:
    try:
        return next(w for w in words if text == w.text)
    except StopIteration:
        return None


def nearest_words(text):
    w = find_word(text, words)
    if not w:
        return "Sorry, I don't know that word."
    else:
        return print_most_similar(words, text)


words = load_words(os.path.join(os.path.dirname(__file__), 'data/wiki-short.vec'))

if __name__ == "__main__":
    print_most_similar(words, words[190].text)
    print_most_similar(words, words[230].text)
    print_most_similar(words, words[330].text)
    print_most_similar(words, words[430].text)

    print("")

    # Related words (interactive)
    while True:
        text = read_word()
        nearest_words(text)
