import os
import csv
import sys


MAX_FILE_NBR = 50
REMOVE_SYMBOLS = [ "" ]
REPLACE_SYMBOLS = [ ".", ",", ":", ";", "!", "?", "(", ")", "\"", "-", " - ", "--", "'", "*", "`" ]

def generate_csv_from_boolean_model(boolean_model: dict, files_name: list[str], words: list[str]):
    with open('boolean_table.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([ '' ] + files_name)
        for word in words:
            writer.writerow([ word ] + [ boolean_model[word][index] for index in range(len(files_name)) ])


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


def get_boolean_model(files_content: dict, words: list[str]):
    files_name = list(files_content.keys())
    boolean_word_table = {}

    for word in words:
        print(word)
        words_boolean = [ word in files_content[files_name[index]] for index in range(len(files_name)) ]
        boolean_word_table[word] = words_boolean

    return boolean_word_table


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        folder_name = sys.argv[1]
        files_name = sorted(os.listdir(folder_name))

        with open("stopwords.txt") as stopwords_file:
            stopwords = [ word.replace('\n', '') for word in stopwords_file.readlines() ]

        folder_words, files_content = get_words_and_content(files_name, stopwords)
        boolean_model = get_boolean_model(files_content, folder_words)

        generate_csv_from_boolean_model(boolean_model, files_name, folder_words)
