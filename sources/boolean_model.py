import os
import csv
import sys


MAX_FILE_NBR = 5
REMOVE_SYMBOLS = [ "" ]
REPLACE_SYMBOLS = [ ".", ",", ":", ";", "!", "?", "(", ")", "\"", "-", " - ", "--", "'", "*", "`" ]

# def generate_csv_from_boolean_model(boolean_model: dict, files_name: list[str], words: list[str]):
#     with open('boolean_table.csv', 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         writer.writerow([ '' ] + files_name)
#         for word in words:
#             writer.writerow([ word ] + [ boolean_model[word][index] for index in range(len(files_name)) ])


def get_file_words(file_path: str, stopwords: list[str]) -> list[str]:
    file_words: list[str] = []

    with open(file_path, "r") as file:
        for line in file.readlines():
            clean_line = line.strip().lower()
            for symbol in REPLACE_SYMBOLS:
                clean_line = clean_line.replace(symbol, " ")
            file_words += clean_line.split(" ")

        file_words = sorted(set(file_words))

        for symbol in REMOVE_SYMBOLS:
            file_words.remove(symbol)

        for stopword in stopwords:
            if stopword in file_words:
                file_words.remove(stopword)

        for word in [ word for word in file_words ]:
            if word.isalpha() == False:
                file_words.remove(word)

    return file_words


def get_words_and_content(files_name: list[str], stopwords: list[str]):
    files_content = {}
    folder_words = []

    for index in range(len(files_name)):
        print(folder_name + "/" + files_name[index])
        file_words = get_file_words(folder_name + "/" + files_name[index], stopwords)
        files_content[files_name[index]] = file_words
        folder_words += file_words
        if index >= MAX_FILE_NBR:
            break

    return sorted(set(folder_words)), files_content


def get_inverted_index_posting_list(files_content: dict, words: list[str], files_name: list[str]):
    posting_list: dict[str, list[int]] = {}

    for word in words:
        posting_list[word] = list()
        for index in range(len(files_name)):
            if word in files_content[files_name[index]]:
                posting_list[word].append(index)

    return posting_list


def get_documents_from_terms(query_terms: list[str], words: list[str], posting_list: dict[str, list[int]]):
    query_documents: list[int] = []

    if len(query_terms) > 1:
        for term in query_terms:
            clean_term = term.strip().lower()
            if clean_term in words:
                print(clean_term, posting_list[clean_term])
                for doc_index in posting_list[clean_term]:
                    query_documents.append(doc_index)

    return query_documents


def query_processing(query: str, files_content: dict, words: list[str], posting_list: dict[str, list[int]]):
    query_documents: list[int] = []
    and_query_terms = query.split(" AND ")
    or_query_terms = query.split(" OR ")

    # AND only
    if len(and_query_terms) > 1:
        query_documents = get_documents_from_terms(and_query_terms, words, posting_list)
        filtered_query_documents = list(filter(lambda item: query_documents.count(item) == len(and_query_terms), query_documents))
        cleaned_query_documents = list(set(filtered_query_documents))
        print(cleaned_query_documents)

    # OR only
    if len(or_query_terms) > 1:
        query_documents = get_documents_from_terms(or_query_terms, words, posting_list)
        cleaned_query_documents = list(set(query_documents))
        print(cleaned_query_documents)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        folder_name = sys.argv[1]
        files_name = sorted(os.listdir(folder_name))

        with open("stopwords.txt") as stopwords_file:
            stopwords = [ word.replace('\n', '') for word in stopwords_file.readlines() ]

        folder_words, files_content = get_words_and_content(files_name, stopwords)
        cleaned_files_name = list(files_content.keys())

        posting_list = get_inverted_index_posting_list(files_content, folder_words, cleaned_files_name)

        # for word in posting_list:
        #     print(word, posting_list[word])

        query_processing(
            "Billy AND Gun",
            files_content,
            folder_words,
            posting_list
        )

        query_processing(
            "Billy OR Willy OR Gun",
            files_content,
            folder_words,
            posting_list
        )
