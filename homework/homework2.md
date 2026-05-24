
# Week2 
https://docs.google.com/presentation/d/16V4bfiWJeum9ocwKph1ua5zlsJ3lUZ1gwBDeaCMK9Mo/edit?slide=id.g23c41adceb3_0_0#slide=id.g23c41adceb3_0_0

# Homework
課題1:https://github.com/maropook/step2/blob/master/homework/task2_1.py
課題1 ドキュメント: https://github.com/maropook/step2/blob/master/homework/task2_1_doc.md
課題2:https://github.com/maropook/step2/blob/master/homework/task2_2.md
課題3:https://github.com/maropook/step2/blob/master/homework/task2_3.md
課題4:https://github.com/maropook/step2/blob/master/homework/task2_4.py
課題4ドキュメント:https://github.com/maropook/step2/blob/master/homework/task2_4_doc.md

# Task1
ほぼ O(1) で動くハッシュテーブルを自分で実装してみよう
「Python の辞書に相当するものをゼロから自分で作る」宿題です
当然 Python の辞書などは使わずに解いてください！！
ヒント 1🤗
put(key, value), get(key), delete(key) の中身を埋めてください
追加・検索・削除
functional_test() が通れば合格です

ヒント 2🤗
データを追加してもほぼ O(1) で動くように再ハッシュを実装しよう
作り方の例：
要素数がテーブルサイズの 70% を上回ったら、テーブルサイズを 2 倍に拡張
要素数がテーブルサイズの 30% を下回ったら、テーブルサイズを半分に縮小
テーブルサイズは奇数（できれば素数）になるよう調整するとハッシュの衝突が減ります

ヒント 3🤗
ハッシュ関数を見直そう
サンプルコードのハッシュ関数は望ましくない
"alice" と "elica" が同じハッシュ値になって衝突
ハッシュの衝突を減らすにはハッシュ関数をどう工夫すればいいでしょう？


# Task2
木構造を使えば O(log N)、ハッシュテーブルを使えばほぼ O(1) で検索・追加・削除を実現することができて、これだけ見ればハッシュテーブルのほうが優れているように見える。ところが現実の大規模なデータベースでは、ハッシュテーブルではなく木構造が使われることが多い。その理由を考えよ。

いくつか重要な理由があるので思いつくだけ書いてください！

### 挑戦クイズ
つねに O(1) で検索・追加・削除できるデータ構造はあるか？🤔
「ない」という答えでも OK です
調べるより考えて！
わかった人は haraken まで Slack で DM ください

# Task3
目標：「もっとも直近にアクセスされた上位 X 個の <URL, Web ページ> の組が保存できるデータ構造」を作ればよい
以下の操作がほぼ O(1) で実現できるようなデータ構造を考える
与えられた <URL, Web ページ> があるかないかを検索
もしない場合、キャッシュ内で一番古い <URL, Web ページ> を捨てて、代わりに与えられた <URL, Web ページ> を追加する

どの <URL, Web ページ> が一番古いかを O(1) で知るために、ハッシュテーブルに工夫を加えて <URL, Web ページ> をアクセスされた順に並べておけばよい

問題：次の操作をほぼ O(1) で実現するデータ構造を考える
与えられた <URL, Web ページ> があるかないかを検索
もしない場合、キャッシュ内で一番古い <URL, Web ページ> を捨てて、代わりに与えられた <URL, Web ページ> を追加する
ヒント：
ハッシュテーブルだけだと順序を管理できないので、別のデータ構造を組み合わせて、X 個の <URL, Web ページ> をアクセスされた順に取り出せるようにする😀

答えを導くのに特別な知識はいりません
キャッシュの動きを整理してよーーーく考えてみてください！(╹◡╹✿)

答えに辿り着くかどうかより「きちんと考えること」が大事なので、「途中まで考えたけどわかんなかった」「O(1)ではないけど動くものならできた！」などの答えで提出してくれて OK です

STEP の授業の価値 = みなさんがどれくらい考えたか

# Task4
宿題 3 のキャッシュを実装してみよう
実際に手を動かしてコードを書いてみるのは大事！
「コードが書ける」ということは「アイディアをきちんと具体化できている」ということ

サンプルコード cache.py
Python の辞書もライブラリも一切使わずに解いてください（＝自分でゼロから高度なデータ構造を実装するのが目的です）
宿題 1 で作った HashTable を使おう！


## Task3 Memo

globalにoldest_urlとnewest_urlを
hash_tableのItemにolder_urlとnewer_urlをもたせる


hashtableに入れるItemにolder, newerのkeyを入れておく
globalにoldest, newestを持っておく
targetのolderはあるがnewerは無いので

tableにないばあい
buckets内のnewestのolderをtargetにする, target.olderをnewestにしてnewest=target
buckets内のoldestのnewerをoldestにする, oldestを削除

tableにある場合
newestの場合, 何も変更無し

oldestの場合, tableにない場合と同じ挙動
その他の場合 targetをnewestにする+前後を修正する必要がある。removeしてnewerに入れればいいだけ
target.newer.older = target.older
target.older.newer = target.newer
newest.newerをtargetにする
target.older = newest
newestのnewerとnewestをtargetにする

新しいものを入れた時size()がX以下の場合はoldest削除しなくてもいい

====

消す
targetを消す
oldestを消す

要素数がすでにXの場合 or targetがすでにある場合削除
newestを消す場合は無い
oldestを消す→ oldestを削除 oldest = oldest.newer
targetを消す→ target.newer.older = target.older, target.older.newer = target.newer
(target消した時の前後関係を管理したり、oldestを記憶するためにolderもnewerも必要)

入れる(size >= xならば削除したらいい)
oldestの更新は必要ない
newest.newer = target, target.older = newest,  newest = target

動きをよく見ていたら、oldestを削除する、またはtargetを削除する+新しいものを追加する


それ以外
課題3 大きさXのhashmapを使用する。valueにはItemsを持ち、next, newer, olderを持つように
globalとしてoldest, newestを持つようにする