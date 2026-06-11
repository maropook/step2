宿題1
find_shortest_path() 関数を書いて、あるページから別のページへの最短経路を出力してください😀
「渋谷」から「小野妹子」にどうたどり着く？
ヒント：
BFS に工夫を入れて最短経路を出せるようにする
collections.deque を使うとスタックやキューが作れます
30 行程度で書けます😀


(BFSで見つかったやつからreturnして)

python3 homework/task4_1.py wikipedia_dataset/pages_small.txt
 wikipedia_dataset/links_small.txt
python3 homework/task4_1.py wikipedia_dataset/pages_medium.txt
 wikipedia_dataset/links_medium.txt
 python3 homework/task4_1.py wikipedia_dataset/pages_large.txt
 wikipedia_dataset/links_large.txt

宿題2
find_most_popular_pages() 関数を書いて、ページランクを計算して重要度の高いページトップ 10 を求めてください
このスライドで「言葉で説明したアルゴリズムを自分で具体化してコードに落とす」のが宿題の意図です
50 行程度で書けます 😀

ヒント
正しさの確認方法
ページランクの分配と更新を何回繰り返しても「全部のノードのページランクの合計値」が一定に保たれることを確認してください
一定にならない場合何かが間違ってます！
Large のデータセットで動かすためには O(N + E) のアルゴリズムが必要です
ページ数：N = 2215900
リンク数：E = 119006494

ページランクの更新が「完全に」収束するのは時間がかかりすぎるので、更新が十分少なくなったら止める

収束条件の作り方の例：
∑(new_pagerank[i] - old_pagerank[i])^2 < 0.01


宿題3(挑戦課題)
Wikipedia のグラフについて「渋谷」から「池袋」まで、同じページを重複して通らない、できるだけ長い経路を発見してください！！

本当の「最長」経路を求めることは困難
最長経路問題は NP 困難と呼ばれる種類の問題で、多項式時間の計算量では解けないことが信じられています（来週の授業で解説します）
なのでグラフ探索アルゴリズムを工夫して「できるだけ長い」経路を発見してください

ヒント：
BFS を使うか？ DFS を使うか？
visited[node]=True に変えるタイミングは？
ノードを訪れる順番を工夫できるか？

宿題 3 のみ AI の使用を認めます 🤗
Coding Agent ではなく Gemini を使うこと
自分が完全に理解して、メンターさんに自分の言葉で完全に説明できるコードのみ使うこと

ただし、AI に頼らずとも今日の授業で解説した知識の範囲内で十分楽しめると思います
ぼくは DFS + BFS + ちょっとした工夫で解きました
70 行くらい

発見した経路長とプログラムを Slack でつぶやいてください！
だれが一番長い経路を発見できるかな？？

===============
途中です。
課題1: https://github.com/maropook/step2/blob/master/homework/task4_1.py
課題2: https://github.com/maropook/step2/blob/master/homework/task4_2.py
課題3: https://github.com/maropook/step2/blob/master/homework/task4_3.py

