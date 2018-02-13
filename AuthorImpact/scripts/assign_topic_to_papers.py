

from gensim import corpora, models
import gensim
from functions.nlp import tokenize_and_clean
from tqdm import tqdm


#this script is used to assign topic to papers
#it uses the models obtained by the extract_topic_lda.py scripts

if __name__ == "__main__":

    path_paper =  '../data/paper_title.txt'
    path_lda_model = '../data/model.lda'
    path_dict = '../data/dictionary.dic'
    path_out = '../data/paper_assigned_topic.txt'
    file_stop_list = '../data/domain_stop_list.txt'

    dictionary = corpora.Dictionary.load(path_dict)
    lda_model = gensim.models.LdaModel.load(path_lda_model)


    with open(file_stop_list, 'r') as f:
        stop_list_domain = set([item.strip() for item in f.readlines()])

    with open(path_paper, 'r') as fin:
        l_title = [item for item in fin.readlines()[1:]]
        l_out = []
        for item in tqdm(l_title):
            paper_id, title = item.split(',')
            title_processed = [item for item in tokenize_and_clean(title.strip()) if item not in stop_list_domain]
            title_processed_idx = dictionary.doc2bow(title_processed)
            # we are only considering papers that are related to the topic of research of the most cited author
            if len(title_processed_idx) > 0:
                topics_distribution = lda_model.get_document_topics(title_processed_idx)
                l_out.append((paper_id,topics_distribution))
        with open(path_out,'w') as fout:
            for id_paper,result in l_out:
                l_topic_pr = [0]*lda_model.num_topics
                for topic_index, topic_pr in result:
                    l_topic_pr[topic_index] = topic_pr
                str = ','.join(list(map(lambda x: '%0.4f'%x,l_topic_pr)))
                fout.write('%s,%s\n' % (id_paper, str))



