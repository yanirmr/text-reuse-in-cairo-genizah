import pandas as pd
import itertools


def split_by_brackets(text: str) -> list:
    '''
    :param text: transcription text with alternatives in parenthesis like "He (She) is nice"
    :return: list of all alternative strings - ["He is nice", "She is nice"]
    '''
    words_list = text.split()
    alter_words = []
    skip_flag = False

    for i in range(len(words_list)):
        if skip_flag:
            skip_flag = False
            continue
        if i == len(words_list) - 1:
            if words_list[i].startswith("("):
                alter_words[-1].append(words_list[i][1:-1])
            else:
                alter_words.append([words_list[i]])
        else:
            if words_list[i + 1].startswith("("):
                alter_words.append([words_list[i], words_list[i + 1][1:-1]])
                skip_flag = True
            elif words_list[i].startswith("("):
                alter_words[-1].append(words_list[i][1:-1])
            else:
                alter_words.append([words_list[i]])

    list_of_tups = list(itertools.product(*alter_words))
    list_of_str = [' '.join(s) for s in list_of_tups]
    return list_of_str


def parse_transcription_file(path: str, min_length_of_line: int = 10) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(columns={"name": "fragment_id"})
    # X is a delimiter in the input file
    df["transcription"] = df["transcription"].str.split("\n")
    df = df.explode("transcription").reset_index(drop=True)
    df["transcription"] = df["transcription"].str.split("X")
    df = df.explode("transcription").reset_index(drop=True)
    df = df[df['transcription'].apply(lambda x: len(str(x)) > min_length_of_line)].reset_index(drop=True)
    df['clean_transcription'] = df['transcription'].apply(split_by_brackets)
    df = df.explode("clean_transcription").reset_index(drop=True)
    df["clean_transcription"] = df["clean_transcription"].str.replace('؟', '')
    df["clean_transcription"] = df["clean_transcription"].str.strip()
    return df
