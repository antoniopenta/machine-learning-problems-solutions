from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
from functions.nlp import *

# this script is extracting the idf for each term in the considered collection

if __name__ == "__main__":

    path_title = '../data/papers_top50.csv'
    path_term_idf = '../data/word_idf_top50.txt'
    mapping_title = {}

    with open(path_title,'r') as f:
        l_title = [item.strip().split(',')[2] for item in f.readlines()[1:]]
        for index, title in enumerate(l_title):
            mapping_title[index] = title

    print("Extracting ..")
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', strip_accents='unicode', tokenizer=tokenize_and_clean)
    t0 = time()
    tfidf_matrix = tfidf_vectorizer.fit_transform(list(mapping_title.values()))
    print("done in %0.3fs." % (time() - t0))
    feature_names = tfidf_vectorizer.get_feature_names()
    list_terms_idf = [(feature_names[index_term],idf_value) for (index_term, idf_value) in
                        zip(range(0, len(tfidf_vectorizer.idf_)), tfidf_vectorizer.idf_)]
    list_terms_idf.sort(key=lambda x: x[1])
    list_terms_idf_str = [','.join([term, str(value)]) for term, value in list_terms_idf]
    with open(path_term_idf, 'w') as fout:
        fout.write('\n'.join(list_terms_idf_str))


