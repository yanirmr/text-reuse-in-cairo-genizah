import unittest

import os
from code import match_finder
import pandas as pd


# TODO: convert os.path -> pathlib
class Ngram(unittest.TestCase):
    def test_ngram_split_for_range_from_string(self):
        example = "I really like python, it's pretty awesome."
        self.assertEqual(len(match_finder.get_ngram_of_text(example, 2, 4)),
                         15)

    def test_ngram_split_for_range_from_file(self):
        test_file = os.path.join("test_data", "mock_text")
        self.assertEqual(len(match_finder.get_ngram_of_text(test_file, 2, 4, path_file=True)),
                         15)


class FuzzySet(unittest.TestCase):
    @unittest.skip("long test skipped")
    def test_init_fuzzyset_performance(self):
        test_file = os.path.join("test_data", "long_medical_text_1.2M_words.txt")
        match_finder.init_fuzzy_set_on_ngrams(test_file, 2, 4)

    def test_search_in_fuzzyset(self):
        test_file = os.path.join("test_data", "mock_text")
        test_fuzzyset = match_finder.init_fuzzy_set_on_ngrams(test_file, 2, 4)
        test_text = "realy like python"
        res = [(0.8947368421052632, 'really like python,')]
        self.assertEqual(match_finder.search_in_fuzzy_set(test_fuzzyset, test_text), res)


class Corpus(unittest.TestCase):
    def test_get_all_text_file_from_corpus(self):
        self.assertEqual(len(match_finder.get_list_of_text_files_in_dir("test_data")), 1)

    def test_return_file_stem_from_corpus(self):
        self.assertEqual((match_finder.get_list_of_text_files_in_dir("test_data")),
                         ["long_medical_text_1.2M_words"])
