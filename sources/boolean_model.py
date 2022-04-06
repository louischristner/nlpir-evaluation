import os
import csv
import sys


REMOVE_SYMBOLS = [ "" ]
REPLACE_SYMBOLS = [ ".", ",", ":", ";", "!", "?", "(", ")", "\"", "-", " - ", "--", "'", "*", "`" ]

def cool_func(file_path: str, stopwords: list[str]) -> list[str]:
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


def cool_func_two(folder_name: str, stopwords: list[str]):
    files_content = {}
    folder_words = []

    for file_name in sorted(os.listdir(folder_name)):
        print(folder_name + "/" + file_name)
        file_words = cool_func(folder_name + "/" + file_name, stopwords)
        files_content[file_name] = file_words
        folder_words += file_words

    folder_words = sorted(set(folder_words))

    print("folder_words sorted")

    files_name = list(files_content.keys())

    boolean_word_table = {}

    print(len(folder_words))

    for word in folder_words:
        words = [ word in files_content[files_name[index]] for index in range(len(files_name)) ]
        boolean_word_table[word] = words
        print(word, words)

    print("boolean word table created")

    with open('boolean_table.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([ '' ] + files_name)
        for word in folder_words:
            writer.writerow([ word ] + [ boolean_word_table[word][index] for index in range(len(files_name)) ])

    print("csv file created")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        first_folder_name = sys.argv[1]
        second_folder_name = sys.argv[2]

        stopwords_file = open("stopwords.txt")
        stopwords = [ word.replace('\n', '') for word in stopwords_file.readlines() ]

        cool_func_two(first_folder_name, stopwords)
