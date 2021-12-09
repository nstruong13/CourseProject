# Project Documentation

Intelligent browsing system that takes topic keywords as input, scrapes web for relevant documents and generates inverted index and visualizations of most frequent relevant words.

## Team Members
1. David Ho - davidsh3
2. Ben Yang - bhyang2
3. Nicholas Truong - ntruong3 (Captain)
4. Jun Zhong - jmzhong2

## Purpose
In research settings where a new project is embarked upon, a researcher might only have a general knowledge of a topic and is familiar with only a limited scope of keywords. Currently, such researchers would query upon keywords he is familiar with in order to browse and pull less-familiar keywords related to the research project. The researcher would then combine the familiar and less-familiar keywords to create more effective queries. This intelligent browsing project seeks to generate statistical visualizations relevant to a limited-keyword query, in order to help the researcher more quickly and more easily discover keywords that would help generate an effective query. The intelligent browsing program would take in some known keywords as input, scrape all docs and create an inverted index of the most frequent relevant words that appear in the docs resulting from the input query, and then generate statistical visualizations of those most frequent relevant words. 

## System Requirements

**Languages and Modules**
-Python 3.7: requests, urllib, sys, string, pandas, requests_html, HTML, HTMLSession, BeautifulSoup, MetaPy, numpy, glob, pathlib, io, os, shutil, seaborn, matplotlib

-Javascript

## Code Sections and Team Contributions

**Web Scraper**: Developed by David Ho

The web scraper adds the user query to Google search url and returns a list of links from the first page of results, removes unwanted sites such as Youtube and more Google pages, as well as duplicate sites. It scrapes sites using Beautiful Soup for body text, removes punctuations and nontext and writes out the results to a .dat file for further processing with MetaPy.
  
**Text Analysis**: Developed by Ben Yang

Using MetaPy, the text outputted from the web scraper is tokenized into unigrams and filtered for stop words, made lowercase, and stemmed. The unigrams are then analyzed by creating an inverted index with lexicon and postings to understand each term's document frequency, term frequency, and term frequency per document. The terms can then be sorted to display the most frequent terms associated with the search query at the top of the list. This analysis will be used for visualizations for the user.

**Data Visualizations**: Developed by Jun Zhong

The visualizations of this project is made to be user friendly, helping the researcher find the terms most research-relevant to terms in her query. With a primary visualization as a heatmap, it visually guides users to the terms that have highest document frequency. It also contains clarifications for users unfamiliar with the terminology we are unfamiliar with in this class: document and term frequency. The secondary visualization is ten subplots describing the postings of each term listed in the primary visualization.

**Chrome Extension**: Developed by Nicholas Truong

The chrome extension can be deployed to the chrome store so that anyone can download the extension; however, to run it locally, you would need to navigate to chrome://extensions/ in your chrome browser. On the top right, enable developer mode. Then, click the button on the left that says “load unpacked” and select the folder chromeExtension from the project directory. This will automatically load the extension into your browser. The extension needs to communicate with an api server to make the request for the query text. If this project was to be scaled out, the server would need to be hosted by a cloud provider such as AWS. For local development and testing, you would need to go into the project directory and run python3 apiServer.py . The api server will automatically spin up and you can now test the chrome extension. Note: the extension can only handle one query request per session. If you are trying multiple queries, please re-click on the extension.

