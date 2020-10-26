import json
import re
from collections import OrderedDict
from tabulate import tabulate
from nltk import word_tokenize
import itertools


def get_content(file_name):

    f = open(file_name)
    file = f.read()
    parsed_file = json.loads(file)
    return parsed_file


def get_terms(index):

    index_list = get_content(index)
    terms = len(index_list)
    return terms


def get_alpha_index(index):

    index_list = get_content(index)
    alpha_index = []
    alpha_index_text = open("files/alpha_index.txt", 'w')
    for token in index_list:
        if not (re.search(r'\d', token[0])):
            alpha_index.append(token)
            print(json.dumps(token), file=alpha_index_text)
    terms = len(alpha_index)
    with open("files/alpha_index.json", mode="w", encoding="utf-8") as myFile:
        json.dump(alpha_index, myFile)

    return terms


def get_lower_case_index(index):

    index_list = get_content(index)
    case_folding_index = []
    temp_index = []
    postings = []
    case_folding_text = open("files/case_folding.txt", 'w')

    for token in index_list:
        if token[0].lower() not in temp_index:
            term = token[0].lower()
            temp_index.append(term)
            for item in index_list:
                if term == item[0].lower():
                    postings.extend(item[1][1])
            unique_postings = sorted(list(OrderedDict.fromkeys(postings.copy())))
            case_folding_index.append([term, [len(unique_postings), unique_postings.copy()]])
            print(json.dumps([term, [len(unique_postings), unique_postings.copy()]]), file=case_folding_text)
            postings.clear()

    temp_index.clear()
    terms = len(case_folding_index)
    with open("files/case_folding.json", mode="w", encoding="utf-8") as myFile:
        json.dump(case_folding_index, myFile)

    return terms


def stopwords_removal(index, stopwords, words):

    index_list = get_content(index)
    stopwords_list = get_content(stopwords)

    if words == 30:
        stopwords_list = stopwords_list[:30]

    stopwords_index = []
    stopwords_index_text = open("files/stopwords_index.txt", 'w')

    for token in index_list:
        if token[0] not in stopwords_list:
            stopwords_index.append(token)
            print(json.dumps(token), file=stopwords_index_text)

    terms = len(stopwords_index)
    with open("files/stopwords_index.json", mode="w", encoding="utf-8") as myFile:
        json.dump(stopwords_index, myFile)

    return terms


def get_postings(index):

    naive_index = get_content(index)
    postings = 0

    for token in naive_index:
        postings += token[1][0]

    return postings


def tabulate_data():

    unfiltered_terms = get_terms("files/naive_indexer.json")
    unfiltered_postings = get_postings("files/naive_indexer.json")
    alpha_terms = get_alpha_index("files/naive_indexer.json")
    alpha_postings = get_postings("files/alpha_index.json")
    case_folding_terms = get_lower_case_index("files/alpha_index.json")
    case_folding_postings = get_postings("files/case_folding.json")
    thirty_stopwords = stopwords_removal("files/case_folding.json", "files/stop_words.json", 30)
    thirty_stopwords_postings = get_postings("files/stopwords_index.json")
    onefifty_stopwords = stopwords_removal("files/case_folding.json", "files/stop_words.json", 150)
    onefifty_stopwords_postings = get_postings("files/stopwords_index.json")
    headers = ["", "Number", "D%", "T%", "Number", "D%", "T%"]
    terms = [unfiltered_terms, alpha_terms, case_folding_terms, thirty_stopwords, onefifty_stopwords]
    postings = [unfiltered_postings, alpha_postings, case_folding_postings, thirty_stopwords_postings, onefifty_stopwords_postings]
    reductions = []
    cumulative = []
    cumulative_postings = []
    get_ratios(terms, reductions, cumulative)
    get_ratios(postings, reductions, cumulative_postings)

    print('{:>30}'.format('terms'), '{:>33}'.format('nonpositional-postings'))

    table = [["Unfiltered", terms[0], '', '', postings[0], '', ''],
             ["no numbers", terms[1], reductions[0], cumulative[0], postings[1], reductions[4], cumulative_postings[0]],
             ["Case folding", terms[2], reductions[1], cumulative[1], postings[2], reductions[5], cumulative_postings[1]],
             ["30 stop words", terms[3], reductions[2], cumulative[2], postings[3], reductions[6], cumulative_postings[2]],
             ["150 stop words", terms[4], reductions[3], cumulative[3], postings[4], reductions[7], cumulative_postings[3]]
             ]

    print(tabulate(table, headers=headers, tablefmt="github"))


def get_ratios(terms, reductions, cumulative):
    cycle = itertools.cycle(terms)
    next(cycle)

    for term in terms:
        if term == terms[-1]:
            break
        elif term == terms[3]:
            next_term = next(cycle)
            reduction = get_percentage(next_term, terms[2])
        else:
            next_term = next(cycle)
            reduction = get_percentage(next_term, term)

        reductions.append(reduction)

        if not cumulative:
            cumulative.append(reduction)
        else:
            increase = cumulative[-1] + reduction
            cumulative.append(increase)


def get_percentage(dividend, divisor):
    reduction = -(100 - round((dividend/divisor)*100))
    return reduction


def generate_list(stopwords):
    f = open(stopwords)
    file = f.read()
    stopwords_list = word_tokenize(file)

    with open("files/stop_words.json", mode="w", encoding="utf-8") as myFile:
        json.dump(stopwords_list, myFile)


tabulate_data()

#generate_list("files/stopwords.txt")
