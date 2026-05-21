import sys
from collections import defaultdict

# WORDS_FILE = "words.txt"
WORDS_FILE = "test_words.txt"


def main(data_file):
    query_words = read_words(data_file)
    dictionary = create_sorted_dictionary(read_words(WORDS_FILE))

    ans_dict = defaultdict(list)
    if not query_words:
        print("no query found")
        return
    for query in query_words:
        anagrams = get_anagram(query, dictionary)
        ans_dict[query] = anagrams

    print(ans_dict.items())


def create_sorted_dictionary(dictionary):
    new_dictionary = []
    for dict_word in dictionary:
        new_dictionary.append((sorted(dict_word), dict_word))
    sorted_new_dictionary = sorted(new_dictionary)
    # print(f"dictionary:{sorted_new_dictionary}")
    return sorted_new_dictionary


def get_anagram(random_word, dictionary):
    N = len(dictionary)
    ans = []
    sorted_random_word = sorted(random_word)
    answer_index = binary_search_word(sorted_random_word, dictionary)
    print(f"answer_index:{answer_index}")
    ans = select_answers(sorted_random_word, answer_index, dictionary)
    return ans


def select_answers(word, answer_index, dictionary):
    ans = []
    if answer_index == -1:
        return ans
    print(answer_index)
    # 答えを見つけたものの、他にも選択肢があるかもしれない
    # dictionaryのindexが一番小さいanagramを探す
    N = len(dictionary)
    current_index = answer_index - 1
    while 0 <= current_index and dictionary[current_index][0] == word:
        ans.append(dictionary[current_index][1])
        current_index -= 1

    current_index = answer_index
    while current_index < N and dictionary[current_index][0] == word:
        ans.append(dictionary[current_index][1])
        current_index += 1
    print(ans)
    return ans


def binary_search_word(word, dictionary):
    # 文字を2文探索でやる
    # 答えを見つけたらtwo pointersをしてもいいかもしれない
    # 文字の先頭から見ていって、マッチ度で見ていく
    # 1つでも一致しない場合はmidを更新
    # 文字が一致する間はwhileで進める、一致しなくなったらqueryが小さいか大きいかで分岐
    # len(word), len(dict) wordの小さい方でloopする
    # returnされなかった場合は
    # 一致してたけどどちらかの文字が足りない
    # query文字が長い場合→left = mid +1
    # query文字が短い場合→right = mid -1
    # 一致でloop抜けたら文字数が同じ、違う、で分岐する
    left, right = 0, len(dictionary)

    while left <= right:
        mid = (left + right) // 2
        dict_word = dictionary[mid][0]
        common_len = min(len(word), len(dict_word))

        for i in range(common_len):
            # print(f"word:{word}, dict_word:{dict_word}")
            # print(
            #     f"left:{left} mid:{mid} right:{right} index:{i} word:{word[i]} dict:{dict_word[i]} query:{word} dict:{dict_word}"
            # )
            char_dict = dict_word[i]
            char_query = word[i]

            if char_dict == char_query:
                if common_len == i + 1:
                    # 一致でloop抜けたら文字数が同じ、違う、で分岐する
                    if len(word) == len(dict_word):
                        print("middle found")
                        return mid
                    elif len(word) > len(dict_word):
                        left = mid + 1
                    else:
                        right = mid - 1
            elif ord(char_dict) > ord(char_query):
                right = mid - 1
                break
            else:
                left = mid + 1
                break
    # print(f"current_target  left:{left} mid:{mid} right:{right} ")
    return -1


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
    # main(sys.argv[1], sys.argv[2])
