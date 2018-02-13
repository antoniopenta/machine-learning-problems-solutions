# this script is used to format the data extracted for the publisher

if __name__ == "__main__":

    path_file = '../data/author_publisher_top50.csv'
    path_out = '../data/author_publisher_top50_formatted.csv'
    with open(path_file,'r') as f:
        l = [item.split(',') for item in f.readlines()[1:]]
        d_author = {}
        for author,pub,count in l:
            if author not in d_author:
                d_author.setdefault(author,[])

            d_author[author].append(('%s(%s)'%(pub,count.strip())))
    with open(path_out,'w') as fout:
        for key in d_author:
            fout.write('%s,%s\n'%(key,'-'.join(d_author[key])))