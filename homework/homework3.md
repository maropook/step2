https://docs.google.com/presentation/d/1DmNxvyvSj_S9AByuMaFzPha7BDwpyjzJw6QElIqLMfY/edit?slide=id.g2375ad78a42_1_450#slide=id.g2375ad78a42_1_450
### Homework
課題1~3: https://github.com/maropook/step2/blob/master/homework/task3_3.py
課題4: https://github.com/maropook/step2/blob/master/homework/task3_4.py
ドキュメント: https://github.com/maropook/step2/blob/master/homework/task3_4.md

聞きたいこと: 
・テストケースが微妙、どこまで細かくやらないといけないのかと圧倒されている
・簡単にテストケースを量産したい
・TOKENの順番がおかしいときにエラーハンドリングを工夫すべきか

### Task1
モジュール化されたプログラムを変更して、「*」「/」に対応しよう (modularized_calculator)
例： 3.0 + 4 * 2 − 1 / 5
不正な入力、負の数はないと仮定してよい
細かい仕様は好きに定義してください

取り組むときのポイント：
モジュール化を意識する（「私の考える最強の美」を追求してください！！）
デバッグするときは「デバッグの鉄則」を意識する

どうやって「*」「/」と「+」「−」の優先度を扱うか？

式を 2 段階で評価すればよい：s
1 回目の評価で「*」「/」を処理
3.0 + 4 * 2 − 1 / 5 ⇒ 3.0 + 8 − 0.2
2 回目の評価で「+」「−」を処理
3.0 + 8 − 0.2 ⇒ 3.6


### Task2
書いたプログラムが正しく動いていることを確認するためのテストケースを追加しよう
できるだけ網羅的に
1
1 + 2
1.0 + 2
1.0 + 2.0

サンプルプログラムの run_test() 関数にテストを追加すれば OK


### Task3
括弧に対応しよう
例:  (3.0 + 4 * (2 − 1)) / 5
テストケースも追加してください
いろいろな解き方があります（5 種類以上）

カッコ(でるまで先に計算する

### Task4
abs(), int(), round() に対応しよう
abs(1-2.2) => 1.2 （絶対値）
int(1.55) => 1（小数を切捨てる）
round(1.55) => 2（四捨五入）

テストケースも追加してください
例: 12 + abs(int(round(1.55) + abs(int(2.3 + 4))))
