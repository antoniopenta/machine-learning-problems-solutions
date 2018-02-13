
from sqlalchemy import create_engine
import pandas as pd

#this script is inserting relevant data in the database


#insert the data in postgres loading the dataframe with pandas
def insert_data(path_data,name_table,engine,sep=','):
    data_frame = pd.read_csv(path_data, header=0, sep=sep, index_col=None)
    print(data_frame.head(10))
    # write on postgres
    data_frame.to_sql(name_table, engine, schema='dblp', if_exists='append', index=False)


if __name__ == "__main__":
    # create the posgres engine, the db sever is in localhost
    engine = create_engine('postgresql://accenture:accenture@localhost:5432/dblp2')
    #insert the data
    path_title = '../data/title_paper.txt'
    title_table = 'paper'
    insert_data(path_title,title_table,engine)

    path_name = '../data/name_author.txt'
    name_table = 'author'
    insert_data(path_name, name_table, engine)

    path_author_of = '../data/relation_author_of.txt'
    author_of_table = 'author_of'
    insert_data(path_author_of, author_of_table, engine)

    path_cites = '../data/relation_cites.txt'
    cites_table = 'cites'
    insert_data(path_cites, cites_table, engine)

    path_author_of = '../data/relation_journal.txt'
    author_of_table = 'journal'
    insert_data(path_author_of, author_of_table, engine)

    path_cites = '../data/relation_book.txt'
    cites_table = 'book'
    insert_data(path_cites, cites_table, engine)

    path_cites = '../data/relation_proceeding.txt'
    cites_table = 'proceedings'
    insert_data(path_cites, cites_table, engine)

    path_cites = '../data/type_object.txt'
    cites_table = 'type'
    insert_data(path_cites, cites_table, engine)

    path_cites = '../data/name_publisher.txt'
    cites_table = 'publisher'
    insert_data(path_cites, cites_table, engine)
