from tkinter import W
from sqwordle.wordscore import Word, WordScorer

if __name__ == "__main__":
    WordScorer.parse_common_word_file()
    WordScorer.score_all_words()
    WordScorer.dump_word_scores_to_disk()
    WordScorer.read_word_scores_from_disk()

    for word in WordScorer._all_scored_words:
        print(word)
