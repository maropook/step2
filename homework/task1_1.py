import sys

"""
usage python3 task1.py <query>
query should be string, len(string) > 0
"""
WORDS_FILE = "../anagram/words.txt"


def main(query):
    dictionary = create_sorted_dictionary(read_words(WORDS_FILE))
    answer_list = get_anagram(query, dictionary)
    print(answer_list)


def get_anagram_with_base_dictionary(query):
    dictionary = create_sorted_dictionary(read_words(WORDS_FILE))
    return get_anagram(query, dictionary)


def create_sorted_dictionary(raw_dictionary):
    dictionary = []
    for word in raw_dictionary:
        dictionary.append((sorted(word), word))
    return sorted(dictionary)


def get_anagram(raw_query, dictionary):
    sorted_query = sorted(raw_query)
    answer_index = binary_search_word(sorted_query, dictionary)
    return get_answer_from_dictionary(sorted_query, answer_index, dictionary)


def binary_search_word(query, dictionary):
    # 文字を2文探索でやる
    # 答えを見つけたらtwo pointersをしてもいいかもしれない
    # 文字の先頭から見ていって、マッチ度で見ていく
    # 1つでも一致しない場合はmidを更新
    # 文字が一致する間はwhileで進める、一致しなくなったらqueryが小さいか大きいかで分岐
    # len(query), len(dict) wordの小さい方でloopする
    # returnされなかった場合は
    # 一致してたけどどちらかの文字が足りない
    # query文字が長い場合→left = mid +1
    # query文字が短い場合→right = mid -1
    # 一致でloop抜けたら文字数が同じ、違う、で分岐する
    if not query or not dictionary:
        return -1
    left, right = 0, len(dictionary) - 1

    while left <= right:
        mid = (left + right) // 2
        dictionary_word = dictionary[mid][0]
        common_length = min(len(query), len(dictionary_word))
        for i in range(common_length):
            if ord(dictionary_word[i]) > ord(query[i]):
                right = mid - 1
                break
            elif ord(dictionary_word[i]) < ord(query[i]):
                left = mid + 1
                break
            else:
                # 現在のcharが一致した場合
                is_last_common_loop = common_length == i + 1
                # 共通した長さまでMAX一致した場合
                if is_last_common_loop:
                    if len(query) == len(dictionary_word):
                        return mid
                    elif len(query) > len(dictionary_word):
                        left = mid + 1
                    else:
                        right = mid - 1
    return -1


def get_answer_from_dictionary(word, answer_index, dictionary):
    ans = []
    if answer_index == -1:
        return ans

    # 見つけたindexより前にあるならそれを足していく
    current_index = answer_index - 1
    while 0 <= current_index and dictionary[current_index][0] == word:
        ans.append(dictionary[current_index][1])
        current_index -= 1

    # 見つけたindex以降のanagramをansに追加
    current_index = answer_index
    while current_index < len(dictionary) and dictionary[current_index][0] == word:
        ans.append(dictionary[current_index][1])
        current_index += 1
    return ans


def read_words(word_file):
    words = []
    with open(word_file) as f:
        for line in f:
            words.append(line.strip("\n"))
    return words


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s query_file output_file" % sys.argv[0])
        exit(1)
    main(sys.argv[1])
