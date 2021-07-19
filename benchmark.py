import re
from evaluator import Evaluator

def pre_process(dataset_filepath):
    """
    This function is to pre-process code-switched datasets files provided by
    the LinCE benchmark. These files are structured the same where utterances
    are separated by an empty-line with each token-language pair is separated
    by a tab. And each pair exist in a standalone line.

    Parameters
    ----------
    dataset_filepath: str
        A filepath where the dataset text file can be read.
    
    Returns
    -------
    utters: list(list):
        A list of utterances which is a list of tags.
    tags: set
        A set of unique tags found in the dataset.
    """
    utters = []
    tags = set()
    with open(dataset_filepath, encoding="utf-8") as fin:
        curr_utter = []
        for line in fin.readlines():
            line = line.strip()
            if line == "":
                if curr_utter != []:
                    utters.append(curr_utter)
                    curr_utter = []
            elif line[0] == '#':
                continue
            else:
                tag = line.split('\t')[1]
                tags.add(tag)
                curr_utter.append(tag)
    return utters, tags


if __name__ == "__main__":
    ev = Evaluator()
    utters, tags = pre_process("./data/lid_spaeng/dev.conll")
    score = ev.evaluate_corpus(utters, tags-{'lang1', 'lang2'})
    print(score)