from functions.nlp import *










# this script is creating the collection of papers for each author
if __name__ == "__main__":

    file_stop_list = '../data/domain_stop_list.txt'
    file_papers = '../data/papers_top50.csv'
    file_collection = '../data/collection_doc_top50.txt'
    with open(file_stop_list, 'r') as f:
        stop_list_domain = set([item.strip() for item in f.readlines()])

    collection = {}
    with open(file_papers, 'r') as f:
        l_title = [item.strip().split(',') for item in f.readlines()[1:]]
        for index, (id, name, title) in enumerate(l_title):
            if id not in collection:
                collection.setdefault(id,[])
            title_processed = [ item for item in tokenize_and_clean(title) if item not in stop_list_domain]
            collection[id].extend(title_processed)

    with open(file_collection,'w') as f:
        for key in collection:
            str =','.join([word.replace(':',' ') for word in collection[key]])
            f.write('%s:%s\n'%(key,str))
