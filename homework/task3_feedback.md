## 宿題 Week3
*, /, (, ), abs, int, round対応をする電卓を作成する←ふくらませる

## Document Feedback
ドキュメント書くなら説明チックでもいい 何がしたい 背景
プロジェクトの説明
Code見るだけだとどの関数がUserに使ってほしいかわからない 
他の人がどの関数をどう呼び出したらいいかわかる 公式ドキュメント Repository Pythonのライブラリ
どういうライブラリなのか、こういう機能持ってる、こういうのもあるけどココだとこういうのができないからこれはできる
なぜこれがあるか、何が目的なのか
入力数式のような文字列一つ、入力想定、tokenizeに文字列を渡す　tokenizeの出力 evaluate→答えが出ます
roundは対応してる これは対応してない
O(N)とかあると嬉しい

#### 型
token
type: "NUMBER", "PLUS", "MINUS", "MULT", "DIV", "ABS", "INT", "ROUND", "LEFT_PARENSIS" or "RIGHT_PARENSIS"
number: int or float(typeがNUMBERの時のみ存在)

#### 関数
read_number
- 文字列と数字が始まるindexを受け取りintまたはfloatを返す
- 対象の文字が数字である限りindexを増やし読み込んでいく
- 小数点・整数に対応

read_*
- typeに*としてtokenを作成しindexを読み込んだ文字の数分増やす

tokenize
- 文字列からtokenのリストを作成する
対応している文字を受け取ってread_*で1つ1つtokenを作成し追加していく

evaluate
- resolve_parenthes, resolve_math_functions, resolve_multi_div, resolve_plus_minus の順番でtokenを処理していき、最後に残ったtype:NUMBER tokenの値を返す

resolve_parenthes
- かっこに囲われた部分を内側のかっこから計算し、かっこを含まないtokensを返す

resolve_parensis
- 開きかっこと閉じかっこを受け取りその中計算して返す、かっこの深さは必ず1

resolve_math_functions
- abs, int, roundを計算し、それらを含まないtokensを返す

resolve_multi_div
- *と/を計算し、それらを含まないtokensを返す

resolve_plus_minus
- +と-を計算し、それらを含まないtokensを返す

test
- 受け取った文字列でeval関数とevaluate関数の結果を比較し絶対値が1e-8より小さければPASSする

run_test
- testを複数呼び出す
