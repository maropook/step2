
### 宿題Week1
https://docs.google.com/presentation/d/15dQHznGo_qUOoz6-NBQlRUAyv7g7C9BpzobDgkLKtO0/edit?slide=id.g12820673c4d_3_0#slide=id.g12820673c4d_3_0


words.pyを辞書とする、辞書を読み込んで配列にしておく
large.txtをinputとする、これを読み込んで配列としておく

N:辞書の単語数, M:単語の長さ

#### 宿題1
与えられた文字列のanagramを辞書ファイルから探して、「見つかったアナグラム全部」を答えるプログラムを作る
自分でテストケースを作って、確認してね♪
# 全列挙 M!
# sortして二分探索 MlogM, NlogN
# 文字列listとして新の辞書を作成し N+logN

#文字列1つをファイルに入れる、ちょうどその文字を使ってるやつ使う

#### 宿題2
会えられた全部の文字使わなくてもいい　タモリ →森(辞書)
# ソートする→使うか使わないを列挙する2^m * logN
# N abcd等の構成要素をカウントし、これらの文字だけで辞書のものが使えるか

与えられた文字列の全ての文字を使わなくても良いように関数をアップデートする。
https://github.com/xharaken/step2/tree/master/anagram
入力：small.txt, large.txt
出力：各入力について「最大のスコアを持つ単語一つ」を列挙したファイル

../anagram/score_checker.py ../anagram/small.txt task1_2_1_ans.txt



### テストケースについて
まずは簡単なテストケースから考えよう
次に極端な例について考えよう（エッジケース）
anagramが複数ある場合は？
anagramが見つからない場合は？
与えられた単語がとても短い場合は？長い場合は？
空の文字列が与えられた時は？ input: “”

#### 宿題3
与えられた文字列から作れる anagram のスコアの合計ができるだけ
        大きくなる複数単語を列挙する
入力：small.txt, large.txt
出力：各入力について「できるだけ大きいスコアになる複数の単語」を空白区切りで列挙したファイル
例："rmoirhgaapocthpo" → "photographic roam"（"microphotograph" 一単語よりスコア合計が高い）
→ 分割した単語だがmergeしたときにうまく行かなければならない
