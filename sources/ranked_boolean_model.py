import os
import sys


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
    files_content = {}
    folder_words = []

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


def get_inverted_index_posting_list(files_content: dict, words: list[str], files_name: list[str]):
    posting_list: dict[str, list[tuple[int, int]]] = {}

    for index in range(len(files_name)):
        file_name = files_name[index]
        file_content = files_content[file_name]

        for word in file_content:
            if not word in posting_list:
                posting_list[word] = list()
            posting_list[word].append((index, file_content[word]))

    return posting_list


def get_documents_from_terms(query_terms: list[str], words: list[str], posting_list: dict[str, list[tuple[int, int]]]):
    query_documents: list[tuple[int, int]] = []

    if len(query_terms) > 1:
        for term in query_terms:
            clean_term = term.strip().lower()
            if clean_term in words:
                for doc_index in posting_list[clean_term]:
                    query_documents.append(doc_index)

    return query_documents


def query_processing(query: str, words: list[str], posting_list: dict[str, list[tuple[int, int]]]):
    query_documents: list[int] = []
    and_query_terms = query.split(" AND ")

    and_query_len = len(and_query_terms)

    # AND only
    if and_query_len > 1:
        unranked_documents = get_documents_from_terms(and_query_terms, words, posting_list)
        unranked_doc_indexes = list(map(lambda item: item[0], unranked_documents))

        filtered_doc_indexes = list(set(filter(lambda item: unranked_doc_indexes.count(item) == and_query_len, unranked_doc_indexes)))
        filtered_documents = list(filter(lambda item: item[0] in filtered_doc_indexes, unranked_documents))

        cumuled_frequency_documents = {}

        for doc in filtered_documents:
            if not doc[0] in cumuled_frequency_documents:
                cumuled_frequency_documents[doc[0]] = 0
            cumuled_frequency_documents[doc[0]] += doc[1]

        sorted_frequency_documents = dict(sorted(cumuled_frequency_documents.items(), key=lambda item: item[1], reverse=True))

        for doc in sorted_frequency_documents:
            query_documents.append((doc, sorted_frequency_documents[doc]))

    return query_documents


def get_files_name_from_query_docs(query_docs: list[tuple[int, int]], files_name: list[str]):
    query_doc_names: list[str] = []

    for doc in query_docs:
        query_doc_names.append(files_name[doc[0]])

    return query_doc_names


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
        cleaned_files_name = list(files_content.keys())

        posting_list = get_inverted_index_posting_list(files_content, words, cleaned_files_name)

        query_docs = query_processing("crime AND money", words, posting_list)
        query_doc_names = get_files_name_from_query_docs(query_docs, cleaned_files_name)

        print("NAME OF THE DOCUMENT        FREQUENCIES SUM\n" + ("-" * 82))
        for index, doc in enumerate(query_docs):
            doc_name = cleaned_files_name[doc[0]]
            if index < MAX_FILE_RESULT:
                print("RESULT:", doc_name, " " * (30 - len(doc_name)), doc[1])

        get_precision_and_recall(query_doc_names)
        get_mean_average_precision(query_doc_names)
