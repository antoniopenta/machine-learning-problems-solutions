
from joblib import Parallel, delayed
from collections import Counter
from itertools import zip_longest
from functions.nlp import  *

# this script is creating a dictionary from all the papers associated to the most cited author


#recipe from https://docs.python.org/3/library/itertools.html#recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def process_group(list_text):
    return [tokenize_and_clean(item) for item in list_text]


if __name__ == "__main__":
    path_title = '../data/papers_top50.csv'
    path_file_dict_word = '../data/dict_word_top50.txt'
    num_cores = 4
    num_groups = 1000

    with open(path_title, 'r') as f:
        print('loading and grouping  data..')
        l_title = [item.strip().split(',')[2] for item in f.readlines()[1:]]
        #partition the data in multiple group for the joblib processing
        group_inputs = list(grouper(l_title,num_groups))
        print('done')
        # use joblib to run the scripts on multiple cores
        print('start processing')
        results = Parallel(n_jobs=num_cores)(delayed(process_group)(g) for g in group_inputs)
        print('done')
        l_term = []
        for item1 in results:
            for item2 in item1:
                l_term.extend(item2)
        dict_term = Counter(l_term)
        list_term = [(key, dict_term[key])for key in dict_term]
        #order the word by their occurances
        list_term.sort(key=lambda key: key[1], reverse=True)
        list_term_string = map(lambda x: ','.join([x[0], str(x[1])]), list_term)
        print('writing the data')
        with open(path_file_dict_word, 'w') as fout:
                fout.write('\n'.join(list_term_string))
