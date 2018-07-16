import pandas as pd
import numpy as np
from nltk import regexp_tokenize
from nltk.stem import WordNetLemmatizer
import re

class LemmaTokenizer(object):
    """
    tokenize text
    """
    def __init__(self):
        self.stopwords = [
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
        "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
        'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
        'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
        'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
        'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
        'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
        'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
        'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
        'about', 'against', 'between', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
        'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
        'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
        'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',
        'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
        'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
        "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma',
        'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
        "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
        'won', "won't", 'wouldn', "wouldn't"
        ]
        self.regexp_tokenize = regexp_tokenize

    def __call__(self, doc):
        if pd.notnull(doc):
            # add words to stoplist, previously punctuations have been removed,
            # so we should do the same for the stoplist
            # we also add the top 10 words in the stoplist, these top 10 words
            # are found after post-processing

            doc_lower = self.lower(doc)
            doc_punct = self.striphtmlpunct(doc_lower)
            doc_tabs = self.striptabs(doc_punct)

            # create stoplist
            stoplist = [self.striphtmlpunct(x)
                        for x in self.stopwords] + [
                            'im', 'ive'] + [
                            'use', 'get', 'like', 'file', 'would', 'way',
                            'code','work', 'want', 'need']

            lemmatized = []
            regex_tokens = self.regexp_tokenize(doc_tabs,
                                                pattern='\w+\S+|\.\w+')

            for word in regex_tokens:
                #for word, p_tags in pos_tag(regex_tokens):
                #convert_pos_tag = convert_tag(p_tags)
                wnl = WordNetLemmatizer()
                lemmatized_word = wnl.lemmatize(word)
                if lemmatized_word not in set(stoplist):
                    lemmatized.append(lemmatized_word)

            return lemmatized

        return pd.Series(doc)

    def striphtmlpunct(self, data):
        # remove html tags, code unnecessary punctuations
        # <.*?> to remove everything between <>
        # [^\w\s+\.\-\#\+] remove punctuations except .-#+
        # (\.{1,3})(?!\S) negative lookahead assertion: only match .{1,3} that
        # is followed by white space
        if pd.notnull(data):
            p = re.compile(r'<.*?>|[^\w\s+\.\-\#\+]')
            res = p.sub('', data)
            pe = re.compile('(\.{1,3})(?!\S)')

            return pe.sub('', res)
        return data

    def striptabs(self, data):
        # remove tabs breaklines
        p = re.compile(r'(\r\n)+|\r+|\n+|\t+/i')
        return p.sub(' ', data)

    def lower(self, data):
        if pd.notnull(data):
            return data.lower()
        return data
