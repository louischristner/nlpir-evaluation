import os
import sys
import random

# libraries used for graph generation only
import matplotlib.pyplot as plt
from wordcloud import WordCloud



# information retrieval

# retrieve file content as a text string
def get_file_content_string(file_path: str) -> str:
    file_content_line = ""
    file = open(file_path, "r")

    for line in file.readlines():
        clean_line = line.lstrip().rstrip()
        if len(clean_line) > 0:
            if clean_line.upper() != clean_line:
                file_content_line += " " + clean_line

    file.close()

    file_content_line = file_content_line.lower()

    for symbol in [ ".", ",", ":", ";", "!", "?", "(", ")", "\"", " - ", "--", "'", "*" ]:
        file_content_line = file_content_line.replace(symbol, ' ')
    return file_content_line


# remove values under a certain amount from a file index dictionary
def get_highest_values_file_index(file_index: dict, amount: int) -> dict:
    tmp_key = ""
    tmp_amount = 0
    tmp_file_index = {}

    for _i in range(amount):
        for key in file_index.keys():
            if file_index[key] > tmp_amount and not key in tmp_file_index.keys():
                tmp_amount = file_index[key]
                tmp_key = key
        tmp_file_index[tmp_key] = tmp_amount
        tmp_amount = 0
        tmp_key = ""
    return tmp_file_index


# get the result of indexing each file text of a folder as a dictionary
def get_folder_file_index(folder_name: str, stopwords: list[str]) -> dict:
    files_index = {}

    for file_name in sorted(os.listdir(folder_name)):
        print(file_name)

        file_content_line = get_file_content_string(folder_name + "/" + file_name)
        file_content_list = file_content_line.split(' ')
        file_index = {}

        for word in file_content_list:
            if len(word) > 0 and not word in stopwords and not word in file_index:
                file_index[word] = file_content_list.count(word)

        for word in file_index:
            if not word in files_index:
                files_index[word] = 0
            files_index[word] += file_index[word]
    return files_index


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        first_folder_name = sys.argv[1]
        second_folder_name = sys.argv[2]

        stopwords_file = open("stopwords.txt")
        stopwords = [ word.replace('\n', '') for word in stopwords_file.readlines() ]

        # first folder
        first_folder_file_index = get_folder_file_index(first_folder_name, stopwords)
        first_folder_highest_values_index = get_highest_values_file_index(first_folder_file_index, 60)

        # second folder
        second_folder_file_index = get_folder_file_index(second_folder_name, stopwords)
        second_folder_highest_values_index = get_highest_values_file_index(second_folder_file_index, 60)

    else: print("USAGE: requires two folder names as argument")
