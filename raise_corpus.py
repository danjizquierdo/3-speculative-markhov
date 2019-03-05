
#!/usr/bin/python
import pandas as pd
import re
import sys
import numpy as np

class Necromancer():

    def __init__(self):
        pass

    def pair_up(self,corpus):
    '''
    Create generator to run through a body of text and collect pairs of words with the
    word that follows them.
    '''
        for word in range(len(corpus)-1):
            yield (corpus[word],corpus[word+1])

    def raise_corpus(self,medium):
    '''
    Read local text bodies taken from Goodreads and create the corpus used by the algorithm 
    to generate Markhov chains.
    '''
        df1=pd.read_csv(f'/Users/flatironschool/blogs/3-speculative-markhov/csvs/fantasy-{medium}.csv')
        df2=pd.read_csv(f'/Users/flatironschool/blogs/3-speculative-markhov/csvs/sci-fi-{medium}.csv')
        df3=pd.read_csv(f'/Users/flatironschool/blogs/3-speculative-markhov/csvs/speculative-{medium}.csv')

        df=df1.append(df2.append(df3))

        corpus=df['0'].str.split()
        d_corpus=''
        # clean up the text by replacing many unnecessary characters as well as odd concatenations 
        for medium in corpus:
            book=' '.join(medium).replace('/','').replace('\\','').replace('"','').replace('-','')
            book=re.sub(r'([a-z/.])([A-Z]{1})',r'\1 \2',book)
            d_corpus=' '.join([d_corpus,book])
        d_corpus=d_corpus.split()
        dictionary={}
        pairs=self.pair_up(d_corpus)
        # run through text and create pairs of words to construct dictionary of options for each word
        for prior,posterior in pairs:
            if prior in dictionary.keys():
                dictionary[prior].append(posterior)
            else:
                dictionary[prior]=[posterior]
        return d_corpus, dictionary

    def shamble(self,d_corpus, dictionary,n_words):
    '''
    Given a body of text, dictionary of words in the text, and an amount of words: generate that number of
    words.
    '''
        # choose a random starting point
        beginning = np.random.choice(d_corpus)
        # might as well make sure it's uppercase
        while beginning.islower():
            beginning = np.random.choice(d_corpus)
        # start the chain
        chain=[beginning]
        # progress through the chain
        for i in range(n_words):
            next_word = np.random.choice(dictionary[chain[-1]])
            # if the word ends a sentence, make sure the next word is capital
            if bool(re.search(r'.*[\.?!]$',chain[-1])):
                while next_word.islower():
                    next_word = np.random.choice(dictionary[chain[-1]])
            chain.append(next_word)
        # join the words in the chain together
        chain=' '.join(chain)
        # cut off the generated text at the end of a sentence if possible
        chain=re.sub(r'(.*[.]).*',r'\1',chain)
        return chain

    @classmethod
    def shambler(cls,medium,words):
    '''
    Given local files with prebuilt corpora and dictionaries, generate text for a number of words 
    for either the medium of titles or descriptions
    '''
        import pickle
        if medium == 'title':
            corpus=pickle.load( open("/Users/flatironschool/blogs/3-speculative-markhov/t_corpus.pkl",'rb'))
            dictionary=pickle.load( open("/Users/flatironschool/blogs/3-speculative-markhov/t_dictionary.pkl",'rb'))
        else:
            corpus=pickle.load( open("/Users/flatironschool/blogs/3-speculative-markhov/d_corpus.pkl",'rb'))
            dictionary=pickle.load( open("/Users/flatironschool/blogs/3-speculative-markhov/d_dictionary.pkl",'rb'))
        n_words=words
        # choose a random starting point
        beginning = np.random.choice(corpus)
        # might as well make sure it's uppercase
        while beginning.islower():
            beginning = np.random.choice(corpus)
        # start the chain
        chain=[beginning]
        # progress through the chain
        for i in range(n_words):
            next_word = np.random.choice(dictionary[chain[-1]])
            # if the word ends a sentence, make sure the next word is capital
            if bool(re.search(r'.*[\.?!]$',chain[-1])):
                while next_word.islower():
                    next_word = np.random.choice(dictionary[chain[-1]])
            chain.append(next_word)
        # join the words in the chain together
        chain=' '.join(chain)
        # cut off the generated text at the end of a sentence if possible
        chain=re.sub(r'(.*[.]).*',r'\1',chain)
        return chain
