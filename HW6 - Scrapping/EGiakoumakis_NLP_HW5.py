# MSDS 7337 - Natural Language Processing
# Homework 5
# Evangelos Giakoumakis

# imports
from requests import get
from bs4 import BeautifulSoup
import nltk
import collections
import csv

# Function to parse the first 25 reviews given a movie link
def movie_review_crawler(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    rev_containers = html_soup.find_all('div', class_ = 'text show-more__control')
    reviews = []
    for rv in rev_containers:
        reviews.append(rv.text)
    return reviews

# Function to create a list of 100 reviews of science fiction movies 
# Films used: (Matrix, Inception, Sunshine, Dragonball)
def my_review_crawler():
        matrix = movie_review_crawler("https://www.imdb.com/title/tt0133093/reviews?ref_=tt_urv")
        inception = movie_review_crawler("https://www.imdb.com/title/tt1375666/reviews?ref_=tt_urv")
        sunshine = movie_review_crawler("https://www.imdb.com/title/tt0448134/reviews?ref_=tt_urv")
        dragonball = movie_review_crawler("https://www.imdb.com/title/tt1098327/reviews?ref_=tt_urv")
        scifi_reviews = matrix + inception + sunshine + dragonball
        return scifi_reviews

# Fetch and place all reviews on list called reviews
reviews = my_review_crawler()

# Function to tokenize and tag texts
def my_tagger(input):
    tokens = nltk.word_tokenize(input)
    tagged = nltk.pos_tag(tokens)
    return tagged

# Place all tagged words to list called tags
tags = []

for i in range(100):    
    tags.append(my_tagger(reviews[i]))

# Function to chunk sentences and show tree
def chunker(tag):
    grammar = ('''
    NP: {<DT>?<JJ>*<NN>} # NP
    ''')
    chunkParser = nltk.RegexpParser(grammar)
    tree = chunkParser.parse(tag)
    for subtree in tree.subtrees():
        return subtree   
    tree.draw()
 
# Place all chunks to list called results
results = []

for x in range(100):      
    results.append(chunker(tags[x]))

# Function to calculate most common words
def sum_text(txt, top_num):
    counts = dict(collections.Counter(txt).most_common(top_num))
    return counts

sum_text(tags[0],25)

# Export chunks to csv file named output 
with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(results)
