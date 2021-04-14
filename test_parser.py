import unittest

import os
from code import parser
import pandas as pd
# TODO: convert os.path -> pathlib


class SplitByBrackets(unittest.TestCase):
    def test_split_by_brackets(self):
        text_no_alternatives = "He is nice"
        list_no_alternatives = ["He is nice"]
        text_one_alternative = "He (She) is nice"
        list_one_alternative = ["He is nice", "She is nice"]
        text_two_alternatives_in_row = "He (She) (It) is nice"
        list_two_alternatives_in_row = ["He is nice", "She is nice", "It is nice"]
        text_two_separate_alternatives = "He (She) is nice (bad)"
        list_two_separate_alternatives = ["He is nice", "She is nice", "He is bad", "She is bad"]
        self.assertEqual(set(parser.split_by_brackets(text_no_alternatives)), set(list_no_alternatives))
        self.assertEqual(set(parser.split_by_brackets(text_one_alternative)), set(list_one_alternative))
        self.assertEqual(set(parser.split_by_brackets(text_two_alternatives_in_row)), set(list_two_alternatives_in_row))
        self.assertEqual(set(parser.split_by_brackets(text_two_separate_alternatives)),
                         set(list_two_separate_alternatives))


class Parser(unittest.TestCase):
    def setUp(self) -> None:
        self.df = parser.parse_transcription_file(os.path.join("test_data", "mock_transcriptions.csv"))

    def test_no_X_and_newline_char_in_clean_transcription(self):
        self.assertEqual((self.df['clean_transcription'].str.contains('X').any()), False)
        self.assertEqual((self.df['clean_transcription'].str.contains('\n').any()), False)

    def test_no_question_mark_in_clean_transcription(self):
        self.assertEqual((self.df['clean_transcription'].str.contains("?", regex=False).any()), False)
        self.assertEqual((self.df['clean_transcription'].str.contains('؟').any()), False)

    def test_no_double_space_in_clean_transcription(self):
        self.assertEqual((self.df['clean_transcription'].str.contains("  ", regex=False).any()), False)

    def test_line_length_over_the_minimum(self):
        self.assertTrue(self.df['clean_transcription'].str.len().min() >= 10)
