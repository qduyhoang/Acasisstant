import os
import json
from nltk import RegexpTokenizer
from smart_open import smart_open
from collections import defaultdict

tokenizer = RegexpTokenizer(r"\w+")
FILE_DIR = 'data/unprocessed'
SAVE_DIR = 'data/processed'
def findDiff(X, Y):
    m = len(X)
    n = len(Y)
    C = defaultdict(lambda:0)
    for i in range(m):
        for j in range(n):
            if X[i] == Y[j]:
                C[i,j] = C[i-1,j-1] + 1
            else:
                C[i,j] = max(C[i, j-1], C[i-1, j])
    deleted, added = [],[]
    i, j = m, n
    while i >= 0 and j >= 0:
        if X[i-1] == Y[j-1]:
        #When two tokens are the same
            i -= 1
            j -= 1
        elif C[i-1,j] >= C[i,j-1]:
            deleted.append((i, X[i-1]))
            i -= 1
        else:
            added.append((j, Y[j-1]))
            j -= 1
    return deleted, added

    

def nlp_clean(data):
    new_data = tokenizer.tokenize(data.lower())
    # new_data = list(set(new_data).difference(stopword_set))
    return new_data
# class MyCorpus(object):
#     def __iter__(self):
#         for line in smart_open(os.path.join(FILE_DIR, 'input'), 'rb'):
#             yield line
# memory_friendly_corpus = MyCorpus()
with smart_open(os.path.join(SAVE_DIR, 'outputfile'), 'a') as output:
    isFirst = True
    first_revision = ''
    for revision in smart_open(os.path.join(FILE_DIR, 'input'), 'rb'):
        if isFirst:
            first_revision = json.loads(revision)['text']
            isFirst = False
        else:
            second_revision = json.loads(revision)['text']
            first_tokens = nlp_clean(first_revision)
            second_tokens = nlp_clean(second_revision)
            # deleted, added = findDiff(first_tokens, second_tokens)
            first_revision = second_revision
            data = {
            'text': first_tokens
            # 'deleted': deleted,
            # 'added': added
            }
            output.write(json.dumps(data))
            output.write('\n')
