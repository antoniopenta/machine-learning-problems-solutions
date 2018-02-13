from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# the wordcloud library is supported only in linux https://github.com/amueller/word_cloud
# I have run the script in a linux machine,
# this script create  word cloud images


if __name__ == "__main__":

    path_collection = '../data/collection_doc_top50.txt'
    path_name_author = '../data/name_author.txt'
    author = {}
    with open(path_name_author, 'r') as f:
        for item in f.readlines():
            key, name = item.split(',')
            if key in author:
                assert (False), 'double key should be not present'
            author[key] = name


    collection = {}
    with open(path_collection,'r') as f:
        for item in f.readlines():
            key, data = item.split(':')
            if key in collection:
                assert (False), 'double key should be not present'
            # Generate a word cloud image
            wordcloud = WordCloud(max_font_size=40).generate(data)
            name = author[key].strip()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.title(name)
            plt.savefig(os.path.join('../data/wc/',name+'.png'))


