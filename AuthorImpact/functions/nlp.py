import nltk
from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer
#in the case of using stemmer
#stemmer = PorterStemmer
#for the lemmatization
wnl = WordNetLemmatizer()
# function uset to tokenize and clean textual data
def tokenize_and_clean(text):
    if text is not None:
        tokens = list(map(lambda x: wnl.lemmatize(x.lower()), nltk.word_tokenize(text)))
        filtered_tokens = [w for w in tokens if w not in stopwords.words('english') and
                           not w.isnumeric() and w not in string.punctuation and len(w)>1]
        return filtered_tokens
    else:
        return ''
