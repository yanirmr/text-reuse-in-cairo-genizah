import match_finder
import code.parser
import pandas as pd
from pathlib import Path
from datetime import datetime


def runner(corpus_dir: str, transcription_file: str) -> None:  # pd.DataFrame:
    """

    :return: dataframe with the next columns: fragment_id, transcription, clean_transcription, URL, match text, extended
    context, title, match grade
    """
    start_time = datetime.now()

    transcription_df = code.parser.parse_transcription_file(transcription_file)
    print(transcription_df.head(15))
    corpus_books_list = match_finder.get_list_of_text_files_in_dir(corpus_dir)
    corpus_path = Path(corpus_dir)

    for ix, book_name in enumerate(corpus_books_list):
        f_set = match_finder.init_fuzzy_set_on_ngrams(corpus_dir + "\\" + book_name + ".txt", 3, 10)

        for phrase in transcription_df["clean_transcription"].iteritems():
            #TODO: complete the function in match finder
            print(match_finder.search_in_fuzzy_set(f_set, phrase[1]))



runner("data", "data/mock_transcriptions.csv")
