# Week3 宿題
## モジュール化した計算機
数式をターミナル上で入力し、文字列として受け取り計算する計算機。
0-9, +, -, *, /, (, ), abs, round, int対応に対応。

### 型
#### `token`
"type"と"number"をkeyとする辞書型。 演算子や記号、数字ごとに作成する。
"type": 演算子や記号、数字かを識別する。"NUMBER", "PLUS", "MINUS", "MULT", "DIV", "ABS", "INT", "ROUND", "L_PAREN" または "R_PAREN"。
"number": typeが"NUMBER"の際の実際の値。整数または少数。

### 関数
#### `tokenize(str) -> tokens`
tokenのlistを返す。引数は文字列。
文字列を演算子や記号と数字に分割しそれぞれtokenに変換する。

#### `read_number(str, index) -> token, index`
引数から作成したtokenと読み取った文字列の数だけ増やしたindexを返す。引数は文字列、数字が始まるindex。数字は整数または小数。

#### `read_operator(str, index) -> token, index`
引数から作成したtokenと読み取った文字列の数だけ増やしたindexを返す。引数は文字列、演算子または組み込み関数が始まるindex。

#### `evaluate(tokens) -> num`
tokensを計算し、その結果を整数または少数で返す。引数はtokenのlist。

#### `resolve_parenthes(tokens) -> tokens`
かっこを含まないtokenのlistを返す。引数はtokenのlist。

#### `resolve_parensis(tokens) -> tokens`
1つのペアのかっこの内側の計算結果を含むtokenを返す。引数は左のかっこから右のかっこまでのtokenのlist。

#### `resolve_math_functions(tokens) -> tokens`
abs, int, roundを含まないtokenのlistを返す。引数はかっこを含まないtokenのlist。

#### `resolve_multi_div(tokens) -> tokens`
*, /を含まないtokenのlistを返す。引数はかっこと組み込み関数を含まないtokenのlist。

#### `resolve_plus_minus(tokens)  -> tokens`
+, -を含まないtokenのlistを返す。引数はかっこ、組み込み関数、+, -を含まないtokenのlist。

#### `test(str)`
受け取った文字列で`eval`と`evaluate`の結果が同じか比較する。

#### `run_test()`
複数の`test(str)`を呼び出す。
