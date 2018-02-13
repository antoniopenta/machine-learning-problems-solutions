from gensim import corpora, models
import gensim
import numpy as np

# this script is used to estimate the number of topics and the iteration step

if __name__ == "__main__":

    path_stop_list_domain = '../data/domain_stop_list.txt'
    path_collection = '../data/collection_doc_top50.txt'
    path_name_author = '../data/name_author.txt'
    author = {}
    num_topics = [10, 20, 50, 100]
    num_words = 10
    passes = [20, 50, 100]

    with open(path_name_author, 'r') as f:
        for item in f.readlines():
            key, name = item.split(',')
            if key in author:
                assert (False), 'double key should be not present'
            author[key] = name


    collection = {}
    author_index_doc = {}
    with open(path_collection,'r') as f:
        for index,item in enumerate(f.readlines()):
            key, data = item.split(':')
            collection[index] = data.split(',')
            author_index_doc[index] = [key, author[key]]


    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(list(collection.values()))

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in list(collection.values())]
    for p in passes:
        print('Passes %d'%p)
        for topics in num_topics:
            # generate LDA model
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topics,
                                                       alpha='auto',
                                                       id2word=dictionary, update_every=0, passes=p)

            coherence_structure = ldamodel.top_topics(corpus, num_words=num_words)
            coherence_structure_value = [item[-1] for item in coherence_structure]
            array = np.array(coherence_structure_value)
            print('Number Topic %d'%topics)
            print('Avg Coherence : %0.5f'%np.mean(array))
            print('Median Coherence: %0.5f'%np.median(array))
            print('Var Cohehrence %0.5f'%np.var(array))

