import pandas as pd
from nltk.util import ngrams
from pathlib import Path
import fuzzyset
from datetime import datetime


def get_ngrams(text: str, n: int) -> list:
    """
    :rtype: list of strings
    """
    n_grams = ngrams(text.split(), n)
    return [' '.join(grams) for grams in n_grams]


def get_ngram_of_text(text: str, min_n: int, max_n: int = None, path_file: bool = False) -> list:
    """
    This function receives text file path and range (by min & nax values) of n's
     and returns list with all n-grams for any n in [min_n, max_n]
    :param text: the input text or the path file
    :param path_file: True if text is path of text file,
    :param min_n: the shortest n-grams
    :param max_n: the longest ngrams, if only one length needed - keep on None
    :return: list of n-grams form text in all lengths.
    """
    if path_file:
        with open(text, "r", encoding="utf-8") as f:
            text = f.read()
    list_of_ngrams = [get_ngrams(text, n) for n in range(min_n, max_n + 1)]
    return [item for ngrams in list_of_ngrams for item in ngrams]


def get_list_of_text_files_in_dir(path: str) -> list:
    corpus_dir = Path(path)
    text_files_paths = list(corpus_dir.glob('*.txt'))
    print(f"There are {len(text_files_paths)} text files in the corpus.")
    return [txt_file.stem for txt_file in list(text_files_paths)]


def init_fuzzy_set_on_ngrams(text_file_path: str, min_n: int, max_n: int) -> fuzzyset.FuzzySet:
    st = datetime.now()
    print(text_file_path)
    fuzzy_set = fuzzyset.FuzzySet()
    ngram_of_text_file = get_ngram_of_text(text_file_path, min_n, max_n, path_file=True)
    for words in ngram_of_text_file:
        fuzzy_set.add(words)
    print(datetime.now() - st)
    return fuzzy_set


def search_in_fuzzy_set(fuzzy_set: fuzzyset.FuzzySet, phrase: str) -> list:
    return fuzzy_set.get(phrase)


def search_in_fuzzy_set_for_df(fuzzy_set: fuzzyset.FuzzySet, transcription_df: pd.DataFrame) -> pd.DataFrame:
    """
        This function receives fuzzy set and  trnascription dataframe and
         and returns new data frame with optional matches (fragment_id, transcription, clean_trans,
                                                            image_URL, match, context, match_source_title,
                                                            match_grade)
        """
    pass


def quick_fuzzy_set():
    # TODO: https://towardsdatascience.com/fuzzy-matching-at-scale-84f2bfd0c536
    pass
