import json


def search_query(query):
    f = open("files/naive_indexer.json")
    file = f.read()
    naive_index = json.loads(file)
    doc_ids = []
    lower_case = query.lower()

    for token in naive_index:
        if lower_case == token[0].lower() or lower_case in token[0].lower():
            doc_ids.extend(token[1][1])

    return doc_ids


def get_query():
    print("please enter your query (only single term): ")
    query = input()
    terminate = False

    while not terminate:

        while not query or ' ' in query:
            print("please enter your query (only single term): ")
            query = input()

        results = search_query(query)

        if not results:
            print("Your query was not found in the index ")
        else:
            print("Your query was found in the following document IDs : ")
            print(*results, sep="\n")

        print("Do you want to query again? (Y/N) ")
        answer = input()
        if answer.lower() == "n":
            terminate = True
        elif answer.lower() == "y":
            print("please enter your query (only single term): ")
            query = input()


get_query()

