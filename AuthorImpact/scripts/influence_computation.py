
from sqlalchemy import create_engine
import pandas as pd


# this script is used to compute the influence on research according to the approach described in the paper
# it requires a connection with the database.


if __name__ == "__main__":

    path_file_paper_assigned_topic = '../data/paper_assigned_topic.txt'
    path_file_author_topic_10_top50 = '../data/author_topic_10_top50.txt'
    path_out = '../data/influence_analysis.txt'
    th = 0.5


    # create the posgres engine, the db sever is in localhost
    engine = create_engine('postgresql://accenture:accenture@localhost:5432/dblp2')

    q1 = '''select id_paper,id_top_author from dblp.paper_citing_top_author;'''
    papers_citing_top_author = pd.read_sql_query(q1, con=engine)
    print(papers_citing_top_author.head(2))
    l_topic_name=['paper_id', 'topic-0', 'topic-1', 'topic-2', 'topic-3', 'topic-4', 'topic-5', 'topic-6', 'topic-7',
                  'topic-8', 'topic-9']
    paper_assigned_topic = pd.read_csv(path_file_paper_assigned_topic,names=l_topic_name ,header=None)
    print(paper_assigned_topic.head(2))
    l_topic_name = ['author_id', 'author_name', 'topic-0', 'topic-1', 'topic-2', 'topic-3', 'topic-4', 'topic-5',
                    'topic-6', 'topic-7',
                    'topic-8', 'topic-9']
    author_topic_10_top50 = pd.read_csv(path_file_author_topic_10_top50, names=l_topic_name, header=None)
    print(author_topic_10_top50.head(2))
    q2 = 'select * from dblp.top_authors'
    top_authors = pd.read_sql_query(q2, con=engine)
    print(top_authors.head(2))


    # filtering only the paper for which the topics have been extracted
    selected_paper_id_4_topic = paper_assigned_topic['paper_id'].tolist()
    papers_citing_top_author_filtered = papers_citing_top_author[papers_citing_top_author['id_paper'].isin(selected_paper_id_4_topic)]

    #create the dictionary of citations for the selected papers
    dict_citation = {}
    for index, row in papers_citing_top_author_filtered.iterrows():
        id_paper, id_top_author = row
        if id_paper not in dict_citation:
            dict_citation.setdefault(id_paper, [])
        dict_citation[id_paper].append(id_top_author)
    #getting the matrix of topics for each paper
    matrix_paper_topic = paper_assigned_topic.ix[:, 'topic-0':].as_matrix()
    #getting the id of the paper
    paper_list = paper_assigned_topic.ix[:, 'paper_id'].tolist()

    for index_author, row_author in top_authors.iterrows():
        id_author,name_author,total_number_citations = row_author
        #getting the topic value for the author
        selection = author_topic_10_top50[author_topic_10_top50['author_id'].isin([id_author])]
        topic_distribution_top_authors = selection.ix[:, 'topic-0':].values[0]
        topic_distribution_top_authors[topic_distribution_top_authors >= th] = 1
        topic_distribution_top_authors[topic_distribution_top_authors < th] = 0
        projection_matrix_paper_topic = matrix_paper_topic.dot(topic_distribution_top_authors)
        projection_matrix_paper_topic[projection_matrix_paper_topic >= th] = 1
        projection_matrix_paper_topic[projection_matrix_paper_topic < th] = 0
        projection_matrix_paper_topic_list=projection_matrix_paper_topic.tolist()
        array_citation = [0] * len(paper_list)
        for index_array_paper, index_paper in enumerate(paper_list):
            if id_author in dict_citation[index_paper]:
                array_citation[index_array_paper] = 1
        #hamming similarity
        influence =len([ 1 for item1,item2 in zip(array_citation,projection_matrix_paper_topic_list) if item1==item2])/len(paper_list)
        print('%s,%0.4f'%(name_author, influence))
