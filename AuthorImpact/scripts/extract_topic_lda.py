from gensim import corpora, models
import gensim


# this script is extracting the topic from the collections and
# it saves the model for further analysis

if __name__ == "__main__":

    path_stop_list_domain = '../data/domain_stop_list.txt'
    path_collection = '../data/collection_doc_top50.txt'
    path_name_author = '../data/name_author.txt'
    path_topic_word = '../data/word_topic_10_top50.txt'
    path_topic_author = '../data/author_topic_10_top50.txt'
    path_model_lda = '../data/model.lda'
    path_dictonary = '../data/dictionary.dic'

    author = {}
    num_topics = 10
    num_words = 10
    passes = 20

    with open(path_name_author, 'r') as f:
        for item in f.readlines():
            key, name = item.split(',')
            if key in author:
                assert (False), 'double key should be not present'
            author[key] = name.strip()


    collection = {}
    author_index_doc = {}
    with open(path_collection,'r') as f:
        for index,item in enumerate(f.readlines()):
            key, data = item.split(':')
            collection[index] = data.split(',')
            author_index_doc[index] = [key, author[key]]


    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(list(collection.values()))
    dictionary.save(path_dictonary)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in list(collection.values())]
    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics,
                                               alpha='auto',
                                               id2word=dictionary, update_every=0, passes=passes)
    ldamodel.save(path_model_lda)

    list_topic_author = []
    for index, text in enumerate(list(collection.values())):
        author_name = author_index_doc[index][1]
        author_index = author_index_doc[index][0]
        topics_author = ldamodel.get_document_topics(dictionary.doc2bow(text))
        list_topic_author.append((author_index,author_name,topics_author))

    with open(path_topic_word, 'w') as fout:
        for index_topic in range(0, num_topics, 1):
            tuple_wordid_pr = ldamodel.get_topic_terms(index_topic, topn=num_words)
            tuple_word = [dictionary.id2token[word_id] for word_id, value in tuple_wordid_pr]
            tuple_word_pr = ['%0.4f'%value for word_id, value in tuple_wordid_pr]
            fout.write('%d,%s\n' %(index_topic,','.join(tuple_word)))
            fout.write('%d,%s\n' % (index_topic, ','.join(tuple_word_pr)))

    with open(path_topic_author, 'w') as fout:
        for author_index,author_name, topic_probs in list_topic_author:
            l_topic = ['0'] * num_topics
            for topicc_index, topic_value in topic_probs:
                l_topic[topicc_index] = '%0.4f'%topic_value
            fout.write('%s,%s,%s\n' % (author_index,author_name,','.join(l_topic)))
