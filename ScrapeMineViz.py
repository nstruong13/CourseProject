import requests
import urllib
import sys
import string
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup

import metapy
import numpy as np
from glob import glob
from pathlib import Path
import io
import os
import shutil

import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_source(url):

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def scrape_google(query):
    query = urllib.parse.quote_plus(query)
    response = get_source('https://www.google.com/search?q=' + query)
    links = list(response.html.absolute_links)

    # remove links to unwanted sites - can add any others
    unwanted_domains = ('https://www.google.',
                      'https://google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.',
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://www.youtube.',
                      'https://twitter.',
                      'https://play.google.',
                      'https://apps.apple.',
                       'https://search.google.')
    for url in links[:]:
        if (url.startswith(unwanted_domains)):
            links.remove(url)

    # remove duplicate sites
    for url1 in links[:]:
        for url2 in links[:]:
            if url1 == url2:
                continue
            if url2.startswith(url1):
                links.remove(url2)
    return links


def scrape_sites(sites):
    sites_words = []
    for url in sites:
        try:
            output = scrape_site(url)
            sites_words.append(output)
        except:
            print("Unable to scrape site:",url)
    return sites_words

def remove_nontext(str):
    str = str.replace(u'\xa0', u'')
    str = str.replace('\n', '')
    str = str.replace('\t', '')
    str = str.replace('\r', ' ')
    str = str.replace('©', '')
    str = str.replace('(', '')
    str = str.replace(')', '')
    str = str.replace('[', '')
    str = str.replace(']', '')
    str = str.replace(':', '')
    str = str.replace('!', '')
    str = str.replace('"', '')
    str = str.replace('~', '')
    str = str.replace('.', ' ')
    str = str.replace(',', '')
    str = str.replace('—', '')
    str = str.replace('–', '')
    str = str.replace('-', ' ')
    str = str.replace('⟶', '')

    if len(str) > 2 and str.endswith('.'):
        str = str.replace('.', '')

    return str

def scrape_site(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    output = []
    for node in soup.findAll('p'):
        for str in node.findAll(text=True):
            str = remove_nontext(str)
            words = str.split(' ')
            for w in words:
                if (w not in string.punctuation):
                    output.append(w)
    return output

def get_text_data(query):
    sites = scrape_google(query)
    scraped_text = scrape_sites(sites)
    with open('scrapedtext.dat','w',encoding='utf-8') as file:
        for doc in scraped_text:
            for word in doc:
                file.write(word)
                file.write(" ")
            file.write('\n')

def tokens_lowercase(doc):
    
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LengthFilter(tok, min=2, max=10000)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)
    ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
    unigrams = ana.analyze(doc)

    tokens = [token for token in tok]
    
    tok.set_content(doc.content())
    tokens, counts = [], []
    n = 0
    for token, count in unigrams.items():
        n+=1
        counts.append(count)
        tokens.append(token)
    return unigrams

def get_visualizations(queryInput):
    get_text_data(queryInput)

    text_file = open('scrapedtext.dat', 'r', encoding = 'utf-8')
    scraped_text = []
    for line in text_file:
        scraped_text.append(line.strip())
    text_file.close()

    #print(scraped_text)

    new_corpus = []
    for document in scraped_text:
        text = document
        #print(text)
        doc = metapy.index.Document()
        doc.content(text)
        #print(doc.content()) #you can access the document string with .content()
        tokens = tokens_lowercase(doc)
        new_corpus.append(tokens)
        #print(tokens)
    #print(new_corpus)


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

    postings = {}
    for key in sorted_lexicon:
        #print(key)
        for document in range(len(new_corpus)):
            #print(document)
            if key in postings and key in new_corpus[document]:
                #print(postings[key])
                postings[key].append([document, new_corpus[document][key]])
            else:
                if key in new_corpus[document]:
                    postings[key] = [[document,new_corpus[document][key]]]
    #print(postings)

    
    
    #Source the first 10 term-doc frequency pairs and their respective posting tables 
    first10 = {k: sorted_lexicon[k] for k in list(sorted_lexicon)[:10]} 
    first10post = {k: postings[k] for k in list(postings)[:10]}

    #Heatmap
    sns.set(rc={"figure.figsize":(3,1.5)})
    sns.set_theme({'font.style':'normal', 'font.serif':'Times New Roman', 'font.weight':"semibold", 'font.size':'5'})

    df = pd.DataFrame(first10)
    df = df.rename(index = {0: 'Document Frequency', 1: 'Total Frequency'})

    g = sns.heatmap(df, cmap="cividis", annot=True, fmt='g')

    g.set_xticklabels(g.get_xmajorticklabels(), fontsize = 5, fontstyle = 'normal', fontweight = "semibold")
    g.set_yticklabels(g.get_ymajorticklabels(), fontsize = 5, fontstyle = 'italic', fontweight = "roman")
    g.set_xlabel("Term", fontsize = 5, fontstyle = 'italic', fontweight = "roman")
    #g.set_title("RESEARCH TERM FINDER", fontsize = 20)

    #g.text(0, 2, "Document Frequency:  Number of sites on the first page of a Google Scholar Search that contain this specific term.", ha="left", fontsize=5, fontweight = "regular")
    #g.text(0, 2, "Total Frequency:           Number of times this term has appeared among all sites on the first page of a Google Scholar Search.", ha="left", fontsize=5, fontweight = "regular")
    
    g.figure.savefig("heatmap.png",dpi=200, bbox_inches = "tight")
    plt.clf()

    #Creating a list of html images of each posting table
    html_hold = []
    for index in first10post:
        dfpost = pd.DataFrame(postings[index])
        dfpost = dfpost.rename(columns = {0: 'Document Number', 1: 'Frequency'})
        df_styled = dfpost.style.background_gradient(subset = 'Frequency').hide_index().set_caption(index).render()
        #created the html script with .render()  Use IPython.display.HTMLdisplay(df_styled) to view.
        html_hold.append(df_styled)
        #dfi.export(df_styled, index+".png") #for saving the graphs as png files.
    return html_hold

if __name__ == "__main__":
    # change query here to user input
    # query = "text mining"
    query = sys.argv[1]
    get_text_data(query)
    '''
    sites = scrape_google(query)
    print(len(sites),'sites scraped for Google search of query:',query,'\n')
    for s in sites:
        print(s,"\n")
    print("----------------------------")
    print("Scraping sites........\n")
    scraped_text = scrape_sites(sites)
    print("----------------------------")
    print('Scraped text.......\n')
    print(scraped_text)
    '''

    
