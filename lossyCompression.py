import json
import re
from collections import OrderedDict
from tabulate import tabulate


def get_terms(preprocessing, index):

    f = open(index)
    file = f.read()
    index_list = json.loads(file)

    if preprocessing == "unfiltered":
        terms = len(index_list)

    elif preprocessing == "no_numbers":

        alpha_index = []
        alpha_index_text = open("files/alpha_index.txt", 'w')
        for token in index_list:
            if not (re.search(r'\d', token[0])):
                alpha_index.append(token)
                print(json.dumps(token), file=alpha_index_text)
        terms = len(alpha_index)
        with open("files/alpha_index.json", mode="w", encoding="utf-8") as myFile:
            json.dump(alpha_index, myFile)

    elif preprocessing == "case_folding":

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


def get_postings(index):
    f = open(index)
    file = f.read()
    naive_index = json.loads(file)
    postings = 0

    for token in naive_index:
        postings += token[1][0]

    return postings


def tabulate_data():

    headers = ["", "Number", "D%", "T%", "Number", "D%", "T%"]
    unfiltered_terms = get_terms("unfiltered", "files/naive_indexer.json")
    unfiltered_postings = get_postings("files/naive_indexer.json")
    alpha_terms = get_terms("no_numbers", "files/naive_indexer.json")
    alpha_postings = get_postings("files/alpha_index.json")
    case_folding_terms = get_terms("case_folding", "files/alpha_index.json")
    case_folding_postings = get_postings("files/case_folding.json")

    print('{:>30}'.format('terms'), end=' ')
    print('{:>33}'.format('nonpositional-postings'))
    table = [["Unfiltered", unfiltered_terms, '', '', unfiltered_postings, '', ''],
             ["no numbers", alpha_terms, -3, -3, alpha_postings, -8, -8],
             ["Case folding", case_folding_terms, -17, -19, case_folding_postings, -30, -24]]

    print(tabulate(table, headers=headers, tablefmt="github"))


tabulate_data()
