import sys, os
from collections import defaultdict

sys.path.append(os.path.abspath(".."))
from anagram.score_checker import calculate_score

"""
usage python3 task1_2.py ../anagram/large.txt
usage python3 task1_2.py ../anagram/small.txt
"""
WORDS_FILE = "../anagram/words.txt"

# 与えられた文字列をすべて使わなくて良い→queryと辞書をalphabetそれぞれいくつ文字使っているかを記憶する
# query > dictionaryでよい タモリ > モリ
# query include dictionary
# query - dictionaryをして、queryのどのindexもマイナスになっていなければ良い
# dictionaryを2次元配列に変換する a,b,c,d,e,f,gとかが入る配列にして、上から順番に見ていって追記していくしかないのでは
# コピーしまくるのは良くなさそう、
# words_listを2次元配列にする len(dict) * 26
# word_counted_dictionary = [[0]*26 for _ in range(len(dictionary))]
# 1つ1つ見ていってだめならreturnするってだけで良さそう
# dictionaryの中身をスコアの高いにosrtして当てはまったら即時returnする

ALPHABET_COUNT = 26


def create_word_aphabet_count(word):
    alphabet_counts = [0] * ALPHABET_COUNT
    for c in word:
        alphabet_counts[ord(c) - ord("a")] += 1
    return alphabet_counts


def create_dictionary_alphabet_count(words):
    alphabet_counts_dict = defaultdict(list)
    for word in words:
        alphabet_counts = [0] * ALPHABET_COUNT
        for c in word:
            alphabet_counts[ord(c) - ord("a")] += 1
        alphabet_counts_dict[word] = alphabet_counts
    return alphabet_counts_dict


def main(data_file):
    dictionary = read_words(WORDS_FILE)
    sorted_dictionary = sorted(
        dictionary, key=lambda x: calculate_score(x), reverse=True
    )
    dictionary_alphabet_counts = create_dictionary_alphabet_count(sorted_dictionary)
    queries = read_words(data_file)
    ans = 0
    for query in queries:
        new_anagram = get_new_anagram(
            create_word_aphabet_count(query), dictionary_alphabet_counts
        )
        score = calculate_score(new_anagram)
        ans += score
        print(f"{query}: new_anagram:{new_anagram}, score:{score}")
    print(ans)


def get_new_anagram(query, dictonary):
    for dict_word, alphabet_count in dictonary.items():
        for i in range(ALPHABET_COUNT):
            if query[i] < alphabet_count[i]:
                break
            if i == ALPHABET_COUNT - 1:
                return dict_word
    return ""


def read_words(word_file):
    words = []
    with open(word_file) as f:
        for line in f:
            words.append(line.strip("\n"))
    return words


def write_words(word_file):
    with open(word_file) as f:
        for line in f:
            print(line, file=f)
    return


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s query_file output_file" % sys.argv[0])
        exit(1)
    main(sys.argv[1])
