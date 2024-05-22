import unittest
import pandas as pd

# Assuming the functions are in a module named text_preprocessing
from cleaner_panda.text_cleaner import (
    remove_common_words,
    convert_to_lowercase,
    remove_punctuation,
    lemmatization,
    expand_contractions,
    remove_special_characters,
    remove_numerical,
    filter_words,
    remove_stopwords,
    stem_words,
    remove_html_tags,
    replace_urls
)

class TestTextPreprocessing(unittest.TestCase):

    def setUp(self):
        # Create a sample dataframe for testing
        self.data = pd.DataFrame({
            'text': [
                "This is a sample text with a URL http://example.com",
                "Here's another text with a number 1234 and an HTML tag <br>",
                "Expanding contractions like don't and won't",
                "Removing punctuation, numbers 567, and special characters $#@!",
                "Some explicit content like fuck that needs filtering"
            ]
        })

    def test_convert_to_lowercase(self):
        df = self.data.copy()
        print("Before converting to lowercase:\n")
        print(df)
        
        result = convert_to_lowercase(df, 'text')
        
        print("\nAfter converting to lowercase:\n")
        print(result)
    
    def test_expand_contractions(self):
        df = self.data.copy()
        print("\nBefore expanding contractions:\n")
        print(df)
        
        result = expand_contractions(df, 'text')
        
        print("\nAfter expanding contractions:\n")
        print(result)
        
    def test_filter_words(self):
        df = self.data.copy()
        print("\nBefore filtering words:\n")
        print(df)
        
        result = filter_words(df, 'text')
        
        print("\nAfter filtering words:\n")
        print(result)
    
    def test_lemmatization(self):
        df = self.data.copy()
        print("\nBefore lemmatization:\n")
        print(df)
        
        result = lemmatization(df, 'text')
        
        print("\nAfter lemmatization:\n")
        print(result)

    def test_remove_common_words(self):
        df = self.data.copy()
        print("\nBefore removing common words:\n")
        print(df)
        
        result = remove_common_words(df, 'text')
        
        print("\nAfter removing common words:\n")
        print(result)

    def test_remove_html_tags(self):
        df = self.data.copy()
        print("\nBefore removing HTML tags:\n")
        print(df)
        
        result = remove_html_tags(df, 'text')
        
        print("\nAfter removing HTML tags:\n")
        print(result)
        
    def test_remove_numerical(self):
        df = self.data.copy()
        print("\nBefore removing numerical values:\n")
        print(df)
        
        result = remove_numerical(df, 'text')
        
        print("\nAfter removing numerical values:\n")
        print(result)

    def test_remove_punctuation(self):
        df = self.data.copy()
        print("\nBefore removing punctuation:\n")
        print(df)
        
        result = remove_punctuation(df, 'text')
        
        print("\nAfter removing punctuation:\n")
        print(result)

    def test_remove_special_characters(self):
        df = self.data.copy()
        print("\nBefore removing special characters:\n")
        print(df)
        
        result = remove_special_characters(df, 'text')
        
        print("\nAfter removing special characters:\n")
        print(result)

    def test_remove_stopwords(self):
        df = self.data.copy()
        print("\nBefore removing stopwords:\n")
        print(df)
        
        result = remove_stopwords(df, 'text')
        
        print("\nAfter removing stopwords:\n")
        print(result)
    
    def test_replace_urls(self):
        df = self.data.copy()
        print("\nBefore replacing URLs:\n")
        print(df)
        
        result = replace_urls(df, 'text')
        
        print("\nAfter replacing URLs:\n")
        print(result)
    
    def test_stem_words(self):
        df = self.data.copy()
        print("\nBefore stemming words:\n")
        print(df)
        
        result = stem_words(df, 'text')
        
        print("\nAfter stemming words:\n")
        print(result)

if __name__ == '__main__':
    unittest.main()