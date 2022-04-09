import os
import sys

from numpy import dot
from math import log, log2
from numpy.linalg import norm


MAX_FILE_NBR = 30
MAX_FILE_RESULT = 15
REMOVE_SYMBOLS = [ "" ]
REPLACE_SYMBOLS = [ ".", ",", ":", ";", "!", "?", "(", ")", "\"", "-", " - ", "--", "'", "*", "`" ]

RELEVANT_DOCUMENTS = [
    "15-Minutes.txt",
    "Absolute-Power.txt",
    "American-Gangster.txt",
    "Birthday-Girl.txt",
    "Big-White,-The.txt",
    "Bling-Ring.txt",
    "Bad-Santa.txt",
    "Bad-Lieutenant.txt",
    "A-Most-Violent-Year.txt",
    "Bad-Country.txt",
    "Black-Rain.txt",
    "American-Hustle.txt",
    "A-Scanner-Darkly.txt",
    "Blood-and-Wine.txt",
    "Batman-2.txt",
    "Batman.txt",
]


def cosine_similarity(vector1: list[float], vector2: list[float]):
    return dot(vector1, vector2) / (norm(vector1) * norm(vector2))


def get_file_words(file_path: str, stopwords: list[str]):
    file_words_frequencies: dict[str, int] = {}

    with open(file_path, "r") as file:
        for line in file.readlines():
            clean_line = line.strip().lower()
            for symbol in REPLACE_SYMBOLS:
                clean_line = clean_line.replace(symbol, " ")
            for word in clean_line.split(" "):
                if not (word in REMOVE_SYMBOLS or word in stopwords or word.isalpha() == False):
                    file_words_frequencies[word] = 1 if not word in file_words_frequencies else file_words_frequencies[word] + 1

    return file_words_frequencies


def get_words_and_content(files_name: list[str], stopwords: list[str]):
    files_content: dict[str, dict[str, int]] = {}
    folder_words: list[str] = []

    for index in range(len(files_name)):
        file_name = files_name[index]
        print("LOAD:", folder_name + "/" + file_name)
        file_words = get_file_words(folder_name + "/" + file_name, stopwords)
        files_content[file_name] = file_words
        folder_words += list(file_words.keys())
        if index + 1 >= MAX_FILE_NBR:
            break

    # force print output
    sys.stdout.flush()

    return sorted(set(folder_words)), files_content


def get_term_document_weight_matrix(files_content: dict[str, dict[str, int]], words: list[str]):
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


def get_query_weight_vector(query: str, documents: dict[str, list[float]], words: list[str], files_content: dict) -> list[float]:
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


def get_precision_and_recall(retrieved_documents: list[str]):
    relevant_retrieved_documents = []
    relevant_not_retrieved_documents = []
    non_relevant_retrieved_documents = []

    for doc in RELEVANT_DOCUMENTS:
        if doc in retrieved_documents:
            relevant_retrieved_documents.append(doc)
        else: relevant_not_retrieved_documents.append(doc)

    for doc in retrieved_documents:
        if not doc in RELEVANT_DOCUMENTS:
            non_relevant_retrieved_documents.append(doc)

    tp = len(relevant_retrieved_documents)
    fp = len(non_relevant_retrieved_documents)
    fn = len(relevant_not_retrieved_documents)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print("PRECISION & RECALL:", precision, recall)


def get_mean_average_precision(retrieved_documents: list[str]):
    cumul_precisions = []

    for index in range(len(retrieved_documents)):
        indexed_retrieved_docs = retrieved_documents[:(index + 1)]

        relevant_retrieved_documents = []
        non_relevant_retrieved_documents = []

        for doc in RELEVANT_DOCUMENTS:
            if doc in indexed_retrieved_docs:
                relevant_retrieved_documents.append(doc)

        for doc in indexed_retrieved_docs:
            if not doc in RELEVANT_DOCUMENTS:
                non_relevant_retrieved_documents.append(doc)

        tp = len(relevant_retrieved_documents)
        fp = len(non_relevant_retrieved_documents)
        cumul_precisions.append(tp / (tp + fp))

    mean_average_precision = sum(cumul_precisions) / len(cumul_precisions)
    print("MEAN AVERAGE PRECISION:", mean_average_precision)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        folder_name = sys.argv[1]
        files_name = sorted(os.listdir(folder_name))

        with open("stopwords.txt") as stopwords_file:
            stopwords = [ word.replace('\n', '') for word in stopwords_file.readlines() ]

        words, files_content = get_words_and_content(files_name, stopwords)
        documents = get_term_document_weight_matrix(files_content, words)

        query_weight_vector = get_query_weight_vector("crime money", documents, words, files_content)
        documents_cos_sin = get_ranked_documents(documents, query_weight_vector)

        print("NAME OF THE DOCUMENT        COSINE SIMILARITY\n" + ("-" * 82))
        for index, doc_name in enumerate(documents_cos_sin):
            if index < MAX_FILE_RESULT:
                if documents_cos_sin[doc_name] > 0.0:
                    print("RESULT:", doc_name, " " * (30 - len(doc_name)), documents_cos_sin[doc_name])

        retrieved_documents = []
        for doc_name in documents_cos_sin:
            if documents_cos_sin[doc_name] > 0.0:
                retrieved_documents.append(doc_name)

        get_precision_and_recall(retrieved_documents)
        get_mean_average_precision(retrieved_documents)
