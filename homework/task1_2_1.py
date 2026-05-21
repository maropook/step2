import sys, os
from collections import defaultdict

sys.path.append(os.path.abspath(".."))
from anagram.score_checker import calculate_score

"""
方法1で実装
usage python3 task1_2_1.py ../anagram/large.txt
usage python3 task1_2_1.py ../anagram/small.txt
"""
WORDS_FILE = "../anagram/words.txt"

ALPHABET_COUNT = 26


def main(data_file, output_file):
    dictionary = create_sorted_dictionary(read_words(WORDS_FILE))
    queries = read_words(data_file)
    ans = 0
    anagrams = []
    for query in queries:
        query_candidates = create_query_substrings("".join(sorted(query)))
        sorted_query_candidates = sorted(
            query_candidates, key=lambda x: calculate_score(x), reverse=True
        )
        new_anagram = get_new_anagram(sorted_query_candidates, dictionary)
        anagrams.append(new_anagram)

        score = calculate_score(new_anagram)
        ans += score
        print(f"query:{query}, new_anagram:{new_anagram}, score:{score}")
    write_words(anagrams, output_file)
    print(ans)


def create_sorted_dictionary(raw_dictionary):
    dictionary = []
    for word in raw_dictionary:
        dictionary.append(("".join(sorted(word)), word))
    return sorted(dictionary)


def create_query_substrings(word):
    N = len(word)
    candidates = []

    # 使うか使わないかでindexを進めていく
    def create_substring(i, current):
        if N == i:
            if current and current not in candidates:
                candidates.append(current)
            return
        create_substring(i + 1, current + "")
        create_substring(i + 1, current + word[i])
        return

    create_substring(0, "")
    return candidates


def get_new_anagram(queries, dictonary):
    for query in queries:
        ans = binary_search_word(query, dictonary)
        if ans:
            return ans
    return ""


def binary_search_word(query, dictionary):
    if not query or not dictionary:
        return ""
    left, right = 0, len(dictionary) - 1

    while left <= right:
        mid = (left + right) // 2
        s_dict_word = dictionary[mid][0]
        dict_word = dictionary[mid][1]

        common_length = min(len(query), len(s_dict_word))

        for i in range(common_length):
            if ord(s_dict_word[i]) > ord(query[i]):
                right = mid - 1
                break
            elif ord(s_dict_word[i]) < ord(query[i]):
                left = mid + 1
                break
            else:
                is_last_common_loop = common_length == i + 1
                if is_last_common_loop:
                    if len(query) == len(s_dict_word):
                        return dict_word
                    elif len(query) > len(s_dict_word):
                        left = mid + 1
                    else:
                        right = mid - 1
    return ""


def read_words(word_file):
    words = []
    with open(word_file) as f:
        for line in f:
            words.append(line.strip("\n"))
    return words


def write_words(words, word_file):
    with open(word_file, "w") as f:
        for word in words:
            print(word, file=f)
    return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s query_file output_file" % sys.argv[0])
        exit(1)
    main(sys.argv[1], sys.argv[2])
