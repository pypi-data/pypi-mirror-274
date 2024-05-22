import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from bs4 import BeautifulSoup
from contractions import contractions_dict

nltk.download('stopwords')
nltk.download('wordnet')

class TextCleaner:
    def __init__(self) -> None:
        pass

lemmatizer = WordNetLemmatizer()

# Remove common words (stopwords)
def remove_common_words(dataframe, column):
    stop_words = set(stopwords.words('english'))
    dataframe[column] = dataframe[column].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
    return dataframe

# Convert text to lowercase
def convert_to_lowercase(dataframe, column):
    dataframe[column] = dataframe[column].str.lower()
    return dataframe

# Remove punctuation
def remove_punctuation(dataframe, column):
    dataframe[column] = dataframe[column].str.replace(r'[^\w\s]', '', regex=True)
    return dataframe

# Lemmatization
def lemmatization(dataframe, column):
    dataframe[column] = dataframe[column].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))
    return dataframe

# Expand contractions
def expand_contractions(dataframe, column):
    contraction_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))
    def expand_text(text):
        def replace(match):
            return contractions_dict[match.group(0)]
        return contraction_re.sub(replace, text)
    dataframe[column] = dataframe[column].apply(lambda x: expand_text(x))
    return dataframe

# Remove special characters
def remove_special_characters(dataframe, column, remove=['.']):
    remove_re = '[' + re.escape(''.join(remove)) + ']'
    dataframe[column] = dataframe[column].str.replace(remove_re, '', regex=True)
    return dataframe

# Remove numerical data
def remove_numerical(dataframe, column):
    dataframe[column] = dataframe[column].str.replace(r'\d+', '', regex=True)
    return dataframe

# Filter out specific words
def filter_words(dataframe, column, remove=['fuck']):
    remove_set = set(remove)
    dataframe[column] = dataframe[column].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in remove_set]))
    return dataframe

# Remove stopwords
def remove_stopwords(dataframe, column):
    stop_words = set(stopwords.words('english'))
    dataframe[column] = dataframe[column].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
    return dataframe

# Stem words
def stem_words(dataframe, column):
    stemmer = PorterStemmer()
    dataframe[column] = dataframe[column].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))
    return dataframe

# Remove HTML tags
def remove_html_tags(dataframe, column):
    dataframe[column] = dataframe[column].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())
    return dataframe

# Replace URLs with a placeholder
def replace_urls(dataframe, column, placeholder='[URL]'):
    url_pattern = re.compile(r'http\S+|www.\S+')
    dataframe[column] = dataframe[column].apply(lambda x: url_pattern.sub(placeholder, x))
    return dataframe