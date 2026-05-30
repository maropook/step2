## 宿題 Week3
コードの説明のドキュメントはどの粒度で書けばいいのか
関数が大まかに何するか
どの様にフローや分岐が進んでいくのかの2点でいいのか
平均時間計算量・空間計算量も必要か

- 
put()
ハッシュを計算し、bucketリストのどこにいれるかを決める
keyがすでにあるかどうか連結リストを探索し確認する
1で決めた箇所の先頭に新たな連結リストを作成する
既存の数値がある場合：valueを書き換える
新しく作る場合：key,valueに引数を代入し、nextに今ある連結リストをつなぐ
平均時間計算量： O(N)
最悪時間計算量： O(N)Nこのキーがあるとする
空間計算量： O(N)Kこのバケット,Qこのバケット内のノード数(K>>Q)

#### 型
- token
type: "NUMBER", "PLUS", "MINUS", "MULT", "DIV", "ABS", "INT", "ROUND", "LEFT_PARENSIS" or "RIGHT_PARENSIS"
number: int or float(typeがNUMBERの時のみ存在)

#### 関数
- read_number
文字列と数字が始まるindexを受け取りintまたはfloatを返す
対象の文字が数字である限りindexを増やし読み込んでいく
小数点・整数に対応

- read_*
typeに*としてtokenを作成しindexを読み込んだ文字の数分増やす

- tokenize
文字列からtokenのリストを作成する
対応している文字を受け取ってread_*で1つ1つtokenを作成し追加していく

- evaluate
resolve_parenthes, resolve_math_functions, resolve_multi_div, resolve_plus_minus の順番でtokenを処理していき、最後に残ったtype:NUMBER tokenの値を返す

- resolve_parenthes
かっこに囲われた部分を内側のかっこから計算し、かっこを含まないtokensを返す

- resolve_parensis
開きかっこと閉じかっこを受け取り、その中計算して返す、かっこの深さは必ず1

- resolve_math_functions
abs, int, roundを計算し、それらを含まないtokensを返す

- resolve_multi_div
*と/を計算し、それらを含まないtokensを返す

- resolve_plus_minus
+と-を計算し、それらを含まないtokensを返す

- test
受け取った文字列でeval関数とevaluate関数の結果を比較し絶対値が1e-8より小さければPASSする

- run_test
testを複数呼び出す
