import metapy
import numpy as np
from glob import glob
from pathlib import Path
import io
import os
import shutil

def tokens_lowercase(doc):
    #Write a token stream that tokenizes with ICUTokenizer (use the argument "suppress_tags=True"), 
    #lowercases, removes words with less than 2 and more than 5  characters
    #performs stemming and creates trigrams (name the final call to ana.analyze as "trigrams")
    '''Place your code here'''
    
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LengthFilter(tok, min=2, max=10000)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)
    ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
    unigrams = ana.analyze(doc)
    #print(unigrams)
    tokens = [token for token in tok]
    
    #leave the rest of the code as is
    tok.set_content(doc.content())
    tokens, counts = [], []
    n = 0
    for token, count in unigrams.items():
        n+=1
        counts.append(count)
        tokens.append(token)
    # print(n)
    # print(counts)
    # print(tokens)
    return unigrams

def pull_files():
    data = []

    for filename in glob("*[1-5].txt"):
        with io.open(filename, mode = 'r', encoding = 'cp437') as f:
            data.append(f.read())

    #data = np.array(data)
    return data

def delete_old_idx():
    location = os.path.abspath(os.getcwd())
    dir = "idx"
    path = os.path.join(location, dir)
    if os.path.isdir(path) == True:
        shutil.rmtree(path)

def create_dat_file(corpus):

    file = open("./google_corpus/google_corpus.dat", "w")
    for document in corpus:
        file.write(document + "\n")
    file.close()


if __name__ == '__main__':

    ## Custom tokenizer and inverted index

    corpus = pull_files()
    #print(corpus)
    create_dat_file(corpus)

    new_corpus = []
    for document in corpus:
        text = document
        doc = metapy.index.Document()
        doc.content(text)
        #print(doc.content()) #you can access the document string with .content()
        tokens = tokens_lowercase(doc)
        new_corpus.append(tokens)
        #print(tokens)
    #print(new_corpus)
    print("\n")


    lexicon = {} # Doc ID, Term --> Frequency
    for document in new_corpus:
        for key in document:
            if key in lexicon:
                lexicon[key][0] += 1
                lexicon[key][1] += document[key]
            else:
                lexicon[key] = [1,document[key]]
            
    lex_list = sorted(lexicon.items(), key=lambda x:x[1], reverse = True)
    sorted_lexicon = dict(lex_list)
    print(sorted_lexicon)
    #print(lexicon)






    ## MetaPy Inverted Index

    # delete_old_idx()

    # cfg = "config.toml"
    # idx = metapy.index.make_inverted_index(cfg)
    # print(idx.num_docs())
    # print(idx.unique_terms())
    # print(idx.avg_doc_length())
    # print(idx.total_corpus_terms())




