#include <cctype>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <filesystem>
#include <unordered_map>

template<typename T>
using my_map = std::unordered_map<std::string, std::vector<T>>;

const int MAX_FILE_NBR = 50;
const char *REMOVE_SYMBOLS[] = { "" };
const char *REPLACE_SYMBOLS[] = {
    ".", ",", ":", ";", "!", "?", "(", ")", "\"", "-", " - ", "--", "'", "*", "`"
};

std::vector<std::string> get_stopwords()
{
    std::string line;
    std::vector<std::string> stopwords;
    std::ifstream file("stopwords.txt");

    if (file.is_open()) {
        while (std::getline(file, line))
            stopwords.push_back(line);
        file.close();
    }

    return stopwords;
}

void ltrim(std::string &str)
{
    str.erase(str.begin(), std::find_if(str.begin(), str.end(), [](unsigned char c) {
        return !std::isspace(c);
    }));
}

void rtrim(std::string &str)
{
    str.erase(std::find_if(str.rbegin(), str.rend(), [](unsigned char c) {
        return !std::isspace(c);
    }).base(), str.end());
}

void trim(std::string &str)
{
    ltrim(str);
    rtrim(str);
}

void str_replace(std::string &str, const std::string &what, const std::string &with)
{
    for (std::string::size_type pos = 0; str.npos != (pos = str.find(what.data(), pos, what.length())); pos += with.length())
        str.replace(pos, what.length(), with.data(), with.length());
}

void vector_erase_str(std::vector<std::string> &vec, const std::string &str)
{
    vec.erase(std::remove(vec.begin(), vec.end(), str), vec.end());
}

bool str_isalpha(const std::string &str)
{
    for (const auto &c : str)
        if (!std::isalpha(c))
            return false;
    return true;
}

void vector_remove_duplicates(std::vector<std::string> &vec)
{
    std::sort(vec.begin(), vec.end());
    vec.erase(std::unique(vec.begin(), vec.end()), vec.end());
}

std::vector<std::string> cool_func(const std::filesystem::path &file_path, const std::vector<std::string> &stopwords)
{
    std::string line;
    std::ifstream file(file_path);
    std::vector<std::string> file_words;

    if (file.is_open()) {
        while(std::getline(file, line)) {
            trim(line);
            std::transform(line.begin(), line.end(), line.begin(),
                [](unsigned char c) { return std::tolower(c); });

            for (const auto &symbol : REPLACE_SYMBOLS)
                str_replace(line, symbol, " ");

            std::istringstream iss(line);
            for (std::string str; iss >> str; )
                file_words.push_back(str);
        }

        vector_remove_duplicates(file_words);

        for (const auto &symbol : REMOVE_SYMBOLS)
            vector_erase_str(file_words, symbol);

        for (const auto &stopword : stopwords)
            vector_erase_str(file_words, stopword);

        // remove non alpha words
        std::vector<std::string> tmp_words;
        std::copy(file_words.begin(), file_words.end(), std::back_inserter(tmp_words));

        for (const auto &word : tmp_words)
            if (str_isalpha(word) == false)
                vector_erase_str(file_words, word);

        file.close();
    }

    return file_words;
}

std::vector<std::string> get_map_keys(const my_map<std::string> &map)
{
    std::vector<std::string> keys;

    keys.reserve(map.size());
    for (const auto &pair : map)
        keys.push_back(pair.first);
    return keys;
}

bool vector_contains_str(const std::vector<std::string> &vec, const std::string &str)
{
    return std::find(vec.begin(), vec.end(), str) != vec.end();
}

my_map<bool> cool_func_two(const std::string &folder_name, const std::vector<std::string> &stopwords)
{
    my_map<bool> boolean_map;
    my_map<std::string> files_content;
    std::vector<std::string> folder_words;
    std::vector<std::filesystem::path> files_in_dir;

    std::copy(std::filesystem::directory_iterator(folder_name), std::filesystem::directory_iterator(), std::back_inserter(files_in_dir));
    std::sort(files_in_dir.begin(), files_in_dir.end());

    for (std::size_t index = 0; index < files_in_dir.size() && index < MAX_FILE_NBR; index++) {
        std::cout << files_in_dir[index] << "\n";

        std::vector<std::string> file_words = cool_func(files_in_dir[index], stopwords);
        folder_words.insert(folder_words.end(), file_words.begin(), file_words.end());
        files_content[files_in_dir[index].stem().string()] = file_words;
    }

    vector_remove_duplicates(folder_words);

    std::vector<std::string> files_name = get_map_keys(files_content);
    std::sort(files_name.begin(), files_name.end());

    for (const auto &word : folder_words) {
        // std::cout << word << "\n";

        boolean_map[word] = std::vector<bool>();
        boolean_map[word].reserve(folder_words.size());
        for (std::size_t index = 0; index < files_name.size(); index++)
            boolean_map[word][index] =
                vector_contains_str(files_content[files_name[index]], word);
    }

    return boolean_map;
}

int main(int ac, char **av)
{
    if (ac >= 3) {
        std::vector<std::string> stopwords = get_stopwords();

        my_map<bool> first_boolean_map = cool_func_two(av[1], stopwords);
        std::cout << first_boolean_map.size() << "\n";

        my_map<bool> second_boolean_map = cool_func_two(av[2], stopwords);
        std::cout << second_boolean_map.size() << "\n";
    }

    return 0;
}