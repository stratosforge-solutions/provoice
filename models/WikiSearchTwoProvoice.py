'''

  Second model that selects important keyword from user input and returns response from Wikipedia.

'''

import json
from textstat.textstat import textstat
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class WikiSearchTwoProvoice():

    # Constructor
    def __init__(self):
        self.id = "wiki_search_two_provoice"
        self.description = "Second model that selects a difficult word from user input and returns" \
                           "a response from Wikipedia, slightly more refined than WikiSearchOne."

    # Helper method to make this class serializable
    def toJson(self):
        response = {}
        response['id'] = self.id
        response['description'] = self.description
        return response

    # The main function of the class.  Works with the API to return a response
    def get_provoice_response(self, input):
        result = {}
        result['input'] = input
        result['model'] = self.toJson()


        responses = []

        # Replace any commas with spaces, so we only have one delimeter character
        input = input.replace(",", " ")

        # Replace any other punctuation  (TODO: There are better ways to do this..)
        input = input.replace("?", " ")
        input = input.replace(".", " ")


        # break up each word in the input
        all_words = input.split(" ")

        # list of all stop words from text file
        # list of words in sentence without stop words
        stopwords = []
        sentencels_no_stopwords = []

        with open('data/stop_words.txt', 'r') as stoptext:
            for word in stoptext:
                word = word.split('\n')
                stopwords.append(word[0])

        sentencels_no_stopwords = [w for w in all_words if w not in stopwords]
        print(sentencels_no_stopwords) #TODO remove when done testing

        hi_score = 0

        for w in sentencels_no_stopwords:
            new_word = w.lower()
            wordscore = textstat.flesch_kincaid_grade(new_word) # TODO can play with another word evaluator
            print("word name is {}, word score is {}".format(w, wordscore))
            if wordscore >= hi_score:
                hi_score = wordscore
                highest_word = new_word
        print("Highest word is {}".format(highest_word))

        url1 = 'https://en.wikipedia.org/w/api.php'
        params = dict(
            action='opensearch',
            search=highest_word,
            limit='20',
            namespace='0',
            format='json'
        )

        resp = requests.get(url=url1, params=params)
        data = resp.json()
        print(data)
        print(type(data))

        for item in data:
            print(item)

        list1 = data[1]

        wiki_hi_score = 0
        i = 0
        wiki_search_index = None
        for item in list1:
            # print(item)
            item_score = textstat.coleman_liau_index(item)
            # print("item name is {}, item score is {}".format(item, item_score))
            if item_score > wiki_hi_score:
                wiki_hi_score = item_score
                winning_wiki_search = item
                wiki_search_index = i
            i = i + 1
        print("Winning wiki search term is {}".format(winning_wiki_search))

        list3 = data[3]
        winning_url = list3[wiki_search_index]

        print("Heading to get {}".format(winning_url))

        resp2 = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params={
                'action': 'query',
                'format': 'json',
                'titles': (winning_wiki_search),
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
            }).json()
        # print(response['query']['pages'].values())
        page = next(iter(resp2['query']['pages'].values()))
        sent = (page['extract'])
        sent_list = sent.split(sep=".")


        highest_word_sentence = []
        new_word_sentence = ""
        hi_score_sentence = 0

        for sentence in sent_list:
            new_word_sentence = sentence.lower()
            wordscore_sentence = textstat.difficult_words(sentence)
            if wordscore_sentence > hi_score_sentence:
                hi_score_sentence = wordscore_sentence
                highest_word_sentence = new_word_sentence

        if hi_score >= 1:
            result['response'] = ("Have you heard of the {}...{}".format(winning_wiki_search, highest_word_sentence))
        else:
            result['response'] = ("Try reading the dictionary bro")


        return result
