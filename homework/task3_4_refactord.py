#! /usr/bin/python3
import traceback

PLUS = "PLUS"
MINUS = "MINUS"
MULT = "MULT"
DIV = "DIV"

ABS = "ABS"
INT = "INT"
ROUND = "ROUND"

L_PAREN = "L_PARE"
R_PAREN = "R_PAREN"

# 0で割ったらまずい問題、数膨大案件→pythonバカでかい数input not a number 例外を投げる
# 関数の定義順はOK
# tokenizeの順番 今回のケース
# やってみないとわからない系のerror case, ぐちゃぐちゃ諦めは必要
# 記号連続はだめ連続したらだめなものabsの後にかっこがない
# ()とかに当てはまるやつ最初に簡易チェックする？残りの深いケース
# helper function みたいなのをつかってそれを中で呼ぶのはいいかも どんなerrorを投げるか？stack traceも表示する
# 10文字目でplusが連続してる　どこで、なんで起きてる?
# Errorが正しく起きるかもテストする TestError作ってエラーのTry catch catchの文面が一緒か
#

operators = {
    "+": {"length": 1, "token": "+", "type": PLUS},
    "-": {"length": 1, "token": "-", "type": MINUS},
    "*": {"length": 1, "token": "*", "type": MULT},
    "/": {"length": 1, "token": "/", "type": DIV},
    "(": {"length": 1, "token": "(", "type": L_PAREN},
    ")": {"length": 1, "token": ")", "type": R_PAREN},
    "a": {"length": 3, "token": "abs", "type": ABS},
    "i": {"length": 3, "token": "int", "type": INT},
    "r": {"length": 5, "token": "round", "type": ROUND},
}


# 文字列を読み取りtokensを返す
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            token, index = read_number(line, index)
        elif line[index] in operators:
            op = operators[line[index]]
            if line[index : index + op["length"]] == op["token"]:
                token, index = {"type": op["type"]}, index + op["length"]
        else:
            print("Invalid character found: " + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# 文字列の数字を受け取りtokenと新たなindexを返す
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == ".":
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {"type": "NUMBER", "number": number}
    return token, index


# 文字列の演算子を受け取りtokenと新たなindexを返す
def read_operator(line, index):
    op = operator[line[index]]
    if line[index : index + op["length"]] == op["token"]:
        return {"type": op["type"]}, index + op["length"]
    else:
        print("Invalid character found: " + line[index])
        exit(1)


# tokensを計算してnumを返す
def evaluate(tokens):
    tokens = resolve_parenthes(tokens)
    # print(f"( and ) were resolved: {tokens}")
    tokens = resolve_math_functions(tokens)
    # print(f"abs, int, round were resolved: {tokens}")
    tokens = resolve_multi_div(tokens)
    # print(f"* and / were resolved: {tokens}")
    tokens = resolve_plus_minus(tokens)
    # print(f"+ and - were resolved: {tokens}")
    return tokens[0]["number"]


# かっこに囲われた部分を内側のかっこから計算し、かっこを含まないtokensを返す
def resolve_parenthes(tokens):
    # 開かっこのindexをstackに入れ、閉じかっこが見つかったらペアのかっこを取得する
    left_parenthes = []
    index = 0
    while index < len(tokens):
        operator = tokens[index]["type"]
        if operator == L_PAREN:
            left_parenthes.append(index)
        elif operator == R_PAREN:
            # 閉じかっこが見つかった、前の開かっこから今の閉じかっこまでを計算してtokenを更新、開かっこと閉じかっこを消して新しい値で上書きする
            left_parenthsis = left_parenthes.pop()
            # 左のかっこから右のかっこまでのtokenをresolve_parensisに渡して計算した値が入ったtokenを得る
            # 速度は重視しないため可読性のためスライスをつかってかっこ前後と計算した値でtokensを構成し直す
            resolved_token = resolve_parensis(tokens, left_parenthsis, index)
            tokens = tokens[:left_parenthsis] + resolved_token + tokens[index + 1 :]
            # 計算したことで不要になった数字や演算子tokenが減ったためindexを調整
            index = left_parenthsis - 1
        index += 1
    return tokens


# 開きかっこと閉じかっこを受け取り、その中計算して返す、かっこの深さは必ず1
def resolve_parensis(tokens, left_parenthesis, right_parenthesis):
    tokens = resolve_math_functions(tokens[left_parenthesis + 1 : right_parenthesis])
    tokens = resolve_multi_div(tokens)
    tokens = resolve_plus_minus(tokens)
    return tokens


# abs, int, roundを計算し、それらを含まないtokensを返す
def resolve_math_functions(tokens):
    index = 1
    while 0 < index < len(tokens):
        operator = tokens[index - 1]["type"]
        if tokens[index]["type"] == "NUMBER" and (
            operator == ABS or operator == INT or operator == ROUND
        ):
            # 計算した値でtokenを上書きする
            number = tokens[index]["number"]
            if operator == ABS:
                tokens[index]["number"] = abs(number)
            elif operator == INT:
                tokens[index]["number"] = int(number)
            elif operator == ROUND:
                tokens[index]["number"] = round(number)
            # 計算し終わった不要な演算子tokenを削除する
            tokens.pop(index - 1)
            index -= 1
        index += 1
    return tokens


# *と/を計算し、それらを含まないtokensを返す
def resolve_multi_div(tokens):
    index = 1
    while 0 < index < len(tokens):
        operator = tokens[index - 1]["type"]
        if tokens[index]["type"] == "NUMBER" and (operator == MULT or operator == DIV):
            first_number = tokens[index - 2]["number"]
            second_number = tokens[index]["number"]
            # 計算した値でtokenを上書きする
            if operator == MULT:
                tokens[index - 2]["number"] = first_number * second_number
            elif operator == DIV:
                tokens[index - 2]["number"] = first_number / second_number
            # 計算し終わった不要な演算子と数tokenを削除する
            tokens.pop(index)
            tokens.pop(index - 1)
            index -= 2
        index += 1
    return tokens


# +と-を計算し、それらを含まないtokensを返す
def resolve_plus_minus(tokens):
    index = 1
    while 0 < index < len(tokens):
        operator = tokens[index - 1]["type"]
        if tokens[index]["type"] == "NUMBER" and (
            operator == PLUS or operator == MINUS
        ):
            first_number = tokens[index - 2]["number"]
            second_number = tokens[index]["number"]
            # 計算した値でtokenを上書きする
            if operator == PLUS:
                tokens[index - 2]["number"] = first_number + second_number
            elif operator == MINUS:
                tokens[index - 2]["number"] = first_number - second_number
            # 計算し終わった不要な演算子と数tokenを削除する
            tokens.pop(index)
            tokens.pop(index - 1)
            index -= 2
        index += 1
    return tokens


# eval関数と作成した電卓の関数の返り値が等しいか確認する
def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print(
            "FAIL! (%s should be %f but was %f)"
            % (line, expected_answer, actual_answer)
        )
        try:
            raise Exception
        except:
            traceback.print_exc()


def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2")
    test("1.0+2.0")
    test("1+2+3")
    test("1.0000+1.00003")

    test("11111111+11111111")
    test("1.0+2.1-3")
    test("11111111-11111111")
    test("1.000-3.99999")
    test("1-2+3-5")

    test("1-2+3-5*0")
    test("15-2+3-5/5")
    test("5/5")
    test("2*3")
    test("3*2")
    test("3.0+4*2-1/5")

    test("(1)")
    test("(1-2)*2")
    test("(1+2+4)*2")
    test("(2)/((1+2+4)*2)+5")

    test("(1)+(2)+(3)")
    test("(1-2)*2")
    test("3/(4*2+4)/2")
    test("3*(2+3*(4+3))")

    test("abs(1-4)")
    test("int(1.2)")
    test("round(3.3)")
    test("12+abs(int(round(1.55)+abs(int(2.3+4))))")
    test("abs(int(round(1.55)+abs(int(2.3+4))))")
    # 見落としがちな値 0
    # 空文字, 負の値どれぐらい
    # 0をどこで使ったらまずいか,
    # 優先順位が正しく処理されているか
    # test_caseの名前も見えるようにするのもあり
    # 基礎
    # コーナーケース

    print("==== Test finished! ====\n")


run_test()

# while True:
#     print("> ", end="")
#     line = input()
#     tokens = tokenize(line)
#     answer = evaluate(tokens)
#     print("answer = %f\n" % answer)

# いろんなアルゴリズム調べる 再帰降下型parser 式をどういう形で書きたいのか？
#
