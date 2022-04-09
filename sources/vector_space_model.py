import os
import sys

from numpy import dot
from math import log, log2
from numpy.linalg import norm

MAX_FILE_NBR = 100
REMOVE_SYMBOLS = [ "" ]
REPLACE_SYMBOLS = [ ".", ",", ":", ";", "!", "?", "(", ")", "\"", "-", " - ", "--", "'", "*", "`" ]

def cosine_similarity(vector1: list[float], vector2: list[float]):
    return dot(vector1, vector2) / (norm(vector1) * norm(vector2))

def get_file_words(file_path: str, stopwords: list[str]) -> dict[str, list[int]]:
    file_words_frequencies: dict[str, list[int]] = {}

    with open(file_path, "r") as file:
        for line in file.readlines():
            clean_line = line.strip().lower()
            for symbol in REPLACE_SYMBOLS:
                clean_line = clean_line.replace(symbol, " ")
            for word in clean_line.split(" "):
                if not (word in REMOVE_SYMBOLS or word in stopwords or word.isalpha() == False):
                    file_words_frequencies[word] = 1 if not word in file_words_frequencies else file_words_frequencies[word] + 1

    return file_words_frequencies


def get_words_and_content(files_name: list[str], stopwords: list[str]) -> tuple[list[str], dict[str, dict[str, list[int]]]]:
    files_content = {}
    folder_words = []

    for index in range(len(files_name)):
        print(folder_name + "/" + files_name[index])
        file_words = get_file_words(folder_name + "/" + files_name[index], stopwords)
        files_content[files_name[index]] = file_words
        folder_words += list(file_words.keys())
        if index >= MAX_FILE_NBR:
            break

    return sorted(set(folder_words)), files_content


def get_term_document_weight_matrix(files_content: dict[str, dict[str, list[int]]], words: list[str]):
    documents: dict[str, list[float]] = {}
    files_amount = len(files_content)
    words_amount = len(words)

    for file_name in files_content:
        documents[file_name] = [0.0] * words_amount
        for word_index in range(words_amount):
            tf, df = 0, 0
            word = words[word_index]
            file_content = files_content[file_name]

            if word in file_content:
                tf = 1 + log(file_content[word])

                for f in files_content:
                    if word in files_content[f]:
                        df += 1

                weight = tf * log2(files_amount / df)
                documents[file_name][word_index] = weight

    return documents


def get_query_weight_vector(query: str, documents: dict[str, list[float]], words: list[str]) -> list[float]:
    words_amount = len(words)
    documents_amount = len(documents)

    query_terms = query.lower().split(" ")
    query_weight_vector = [0.0] * words_amount
    query_terms_frequencies: dict[str, int] = {}

    for query_term in query_terms:
        if query_term in query_terms_frequencies:
            query_terms_frequencies[query_term] += 1
        else: query_terms_frequencies[query_term] = 1

    for word_index in range(words_amount):
        tf, df = 0, 0
        word = words[word_index]

        if word in query_terms:
            tf = 1 + log(query_terms_frequencies[word])

            for f in files_content:
                if word in files_content[f]:
                    df += 1

            weight = tf * log2(documents_amount / df)
            query_weight_vector[word_index] = weight

    return query_weight_vector


def get_ranked_documents(documents: dict[str, list[float]], query_weight_vector: list[float]) -> dict[str, float]:
    documents_cos_sin: dict[str, float] = {}

    for doc_name in documents:
        document = documents[doc_name]
        documents_cos_sin[doc_name] = cosine_similarity(document, query_weight_vector)

    return dict(sorted(documents_cos_sin.items(), key=lambda item: item[1], reverse=True))


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        folder_name = sys.argv[1]
        files_name = sorted(os.listdir(folder_name))

        with open("stopwords.txt") as stopwords_file:
            stopwords = [ word.replace('\n', '') for word in stopwords_file.readlines() ]

        words, files_content = get_words_and_content(files_name, stopwords)
        documents = get_term_document_weight_matrix(files_content, words)

        query_weight_vector = get_query_weight_vector("billy willy", documents, words)
        documents_cos_sin = get_ranked_documents(documents, query_weight_vector)

        for doc_name in documents_cos_sin:
            print(doc_name, documents_cos_sin[doc_name])


