import requests
import urllib
import sys
import string
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup


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
                      'https://apps.apple.')
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
