import nltk
from nltk.corpus import stopwords
import os
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import re

delimiters = [",", "\'\'", "``", "#", "$", "(", ")", ".", ":", ";", "%", "-", "}", "{", "!", "!!", "!!!", "\""]
adjectives = ['JJ', 'JJR', 'JJS']
nouns = ['NNP', 'NN', 'NNS', 'NNPS']
search_list = ["searches", "searching", "seach", "searched", "google", "find", "query", "keyword", "searcher",
               "finding", "search"]
sia = SIA()


def tagger(txt):
    '''
    tokenizes a string and tags it with parts of speech.
    '''
    # f = open(os.path.join(os.path.dirname(__file__), 'inp.txt'), 'r')
    # txt = f.readline()
    # f.close()

    # Word tokenizers is used to find the words
    # and punctuation in a string
    wordslist = nltk.word_tokenize(txt)
    wordslist = [w for w in wordslist]

    # Using a Tagger. Which is part-of-speech
    # tagger or POS-tagger.
    tagged = nltk.pos_tag(wordslist)

    # Uncomment the below line to see the tags
    print(tagged)
    return tagged


def remove_delimiters(tokens):
    '''
    Utility function to clean tokens by delimiters
    '''
    return [tup for tup in tokens if tup[0] not in delimiters]


def remove_stopwords(tokens):
    '''
    Utility function to clean tokens by stopwords
    '''
    stopwords_list = stopwords.words('english')
    return [tup for tup in tokens if tup[0] not in stopwords_list]


def clean(unclean_tokens):
    '''
    cleans the tokens of delimiters, stopwords, and removes search related terms and lower cases them.
    returns a list of dictionaries containing noun and adjectives specific to the given noun.
    '''
    result = []
    unclean_tokens = remove_delimiters(unclean_tokens)
    unclean_tokens = remove_stopwords(unclean_tokens)
    unclean_tokens = to_small(unclean_tokens)
    tokens = remove_search(unclean_tokens)

    # print(tokens)
    for ind, token in enumerate(tokens):
        if token[1] in adjectives:
            if ind + 1 < len(tokens) and tokens[ind + 1][1] in nouns:
                result.append({'adjective': token[0],
                               'noun': tokens[ind + 1][0]
                               })
        elif ind == 0 or (
                token[1] in nouns and ind - 1 >= 0 and tokens[ind - 1][1] not in adjectives):
            result.append({'noun': token[0]
                           })

    return result


def remove_search(tokens):
    '''
    removes search related terms.
    '''
    return [tup for tup in tokens if tup[0] not in search_list]


def to_small(tokens):
    '''
    converts input tokens to lower case.
    '''
    return [(tup[0].lower(), tup[1]) for tup in tokens]


def clean_tokens(txt):
    raw_tokens = tagger(txt)
    results = clean(raw_tokens)
    return results


# prints sentiment of the parameter.
def adjective_sentiment(word):
    score = sia.polarity_scores(word)
    for w in score.keys():
        print(w, score[w])


# POS tag list:
#
# CC	coordinating conjunction
# CD	cardinal digit
# DT	determiner
# EX	existential there (like: "there is" ... think of it like "there exists")
# FW	foreign word
# IN	preposition/subordinating conjunction
# JJ	adjective	'big'
# JJR	adjective, comparative	'bigger'
# JJS	adjective, superlative	'biggest'
# LS	list marker	1)
# MD	modal	could, will
# NN	noun, singular 'desk'
# NNS	noun plural	'desks'
# NNP	proper noun, singular	'Harrison'
# NNPS	proper noun, plural	'Americans'
# PDT	predeterminer	'all the kids'
# POS	possessive ending	parent\'s
# PRP	personal pronoun	I, he, she
# PRP$	possessive pronoun	my, his, hers
# RB	adverb	very, silently,
# RBR	adverb, comparative	better
# RBS	adverb, superlative	best
# RP	particle	give up
# TO	to	go 'to' the store.
# UH	interjection	errrrrrrrm
# VB	verb, base form	take
# VBD	verb, past tense	took
# VBG	verb, gerund/present participle	taking
# VBN	verb, past participle	taken
# VBP	verb, sing. present, non-3d	take
# VBZ	verb, 3rd person sing. present	takes
# WDT	wh-determiner	which
# WP	wh-pronoun	who, what
# WP$	possessive wh-pronoun	whose
# WRB	wh-adverb	where, when

if __name__ == '__main__':
    result = clean(tagger("search for a checked  shirt"))
    for i in range(len(result)):
        print(result[i]['adjective'] if 'adjective' in result[i] else "", result[i]['noun'])
        # if 'adjective' in result[i]:
        #     score = sia.polarity_scores(result[i]['adjective'])
        #     for w in score.keys():
        #         print(w, score[w])
        #     print()
