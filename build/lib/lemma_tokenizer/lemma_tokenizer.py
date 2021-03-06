import pandas as pd
import numpy as np
from nltk import regexp_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pdb
import re

class LemmaTokenizer(object):
    """
    tokenize text
    """
    def __init__(self):
        pass

    def __call__(self, doc):
        if pd.notnull(doc):
            # add words to stoplist, previously punctuations have been removed,
            # so we should do the same for the stoplist
            # we also add the top 10 words in the stoplist, these top 10 words
            # are found after post-processing

            doc_lower = self.lower(doc)
            doc_xcode = self.stripcode(doc_lower)
            doc_punct = self.striphtmlpunct(doc_xcode)
            doc_tabs = self.striptabs(doc_punct)
            # create stoplist
            stoplist = [self.striphtmlpunct(x)
                        for x in stopwords.words('english')] + [
                            'im', 'ive'] + [
                            'use', 'get', 'like', 'file', 'would', 'way',
                            'code','work', 'want', 'need']

            lemmatized = []
            regex_tokens = regexp_tokenize(doc_tabs,
                                                pattern='\w+\S+|\.\w+')
            wnl = WordNetLemmatizer()

            for word, p_tags in pos_tag(regex_tokens):
                convert_pos_tag = self.convert_tag(p_tags)
                lemmatized_word = wnl.lemmatize(word, pos = convert_pos_tag)
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

    def stripcode(self,data):
        # remove code
        p = re.compile("<code>(.+?)<\/code>", flags=re.DOTALL)

        return p.sub('', data)


    def striptabs(self, data):
        # remove tabs breaklines
        p = re.compile(r'(\r\n)+|\r+|\n+|\t+/i')
        return p.sub(' ', data)

    def lower(self, data):
        if pd.notnull(data):
            return data.lower()
        return data

    def convert_tag(self, tag):
        """
        Convert the tag given by nltk.pos_tag
        to the tag used by wordnet.synsets
        """
        tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}
        try:
            return tag_dict[tag[0]]
        except KeyError:
            # defalut value
            return 'n'  #None
