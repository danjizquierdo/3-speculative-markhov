
#!/usr/bin/python
import pandas as pd
import re
import sys
import numpy as np

class Necromancer():

    def __init__(self):
        pass

    def pair_up(self,corpus):
        for word in range(len(corpus)-1):
            yield (corpus[word],corpus[word+1])

    def raise_corpus(self,medium):
        df1=pd.read_csv(f'/Users/flatironschool/blogs/3-speculative-markhov/csvs/fantasy-{medium}.csv')
        df2=pd.read_csv(f'/Users/flatironschool/blogs/3-speculative-markhov/csvs/sci-fi-{medium}.csv')
        df3=pd.read_csv(f'/Users/flatironschool/blogs/3-speculative-markhov/csvs/speculative-{medium}.csv')

        df=df1.append(df2.append(df3))

        corpus=df['0'].str.split()
        d_corpus=''

        for medium in corpus:
            book=' '.join(medium).replace('/','').replace('\\','').replace('"','').replace('-','')
            book=re.sub(r'([a-z/.])([A-Z]{1})',r'\1 \2',book)
            d_corpus=' '.join([d_corpus,book])
        d_corpus=d_corpus.split()
        dictionary={}
        pairs=self.pair_up(d_corpus)

        for prior,posterior in pairs:
            if prior in dictionary.keys():
                dictionary[prior].append(posterior)
            else:
                dictionary[prior]=[posterior]
        return d_corpus, dictionary

    def shamble(self,d_corpus, dictionary,n_words):
        beginning = np.random.choice(d_corpus)

        while beginning.islower():
            beginning = np.random.choice(d_corpus)

        chain=[beginning]

        for i in range(n_words):
            next_word = np.random.choice(dictionary[chain[-1]])
            if bool(re.search(r'.*[\.?!]$',chain[-1])):
                while next_word.islower():
                    next_word = np.random.choice(dictionary[chain[-1]])
            chain.append(next_word)
        chain=' '.join(chain)
        chain=re.sub(r'(.*[.]).*',r'\1',chain)
        return chain

    @classmethod
    def shambler(cls,medium,words):
        import pickle
        if medium == 'title':
            corpus=pickle.load( open("/Users/flatironschool/blogs/3-speculative-markhov/t_corpus.pkl",'rb'))
            dictionary=pickle.load( open("/Users/flatironschool/blogs/3-speculative-markhov/t_dictionary.pkl",'rb'))
        else:
            corpus=pickle.load( open("/Users/flatironschool/blogs/3-speculative-markhov/d_corpus.pkl",'rb'))
            dictionary=pickle.load( open("/Users/flatironschool/blogs/3-speculative-markhov/d_dictionary.pkl",'rb'))
        n_words=words
        beginning = np.random.choice(corpus)
        
        while beginning.islower():
            beginning = np.random.choice(corpus)
    
        chain=[beginning]
        
        for i in range(n_words):
            next_word = np.random.choice(dictionary[chain[-1]])
            if bool(re.search(r'.*[\.?!]$',chain[-1])):
                while next_word.islower():
                    next_word = np.random.choice(dictionary[chain[-1]])
            chain.append(next_word)
        chain=' '.join(chain)
        chain=re.sub(r'(.*[.]).*',r'\1',chain)
        return chain
