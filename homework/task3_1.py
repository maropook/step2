#! /usr/bin/python3


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


PLUS_TOKEN = "PLUS"
MINUS_TOKEN = "MINUS"
MULT_TOKEN = "MULT"
DIV_TOKEN = "DIV"


def read_plus(line, index):
    token = {"type": PLUS_TOKEN}
    return token, index + 1


def read_minus(line, index):
    token = {"type": MINUS_TOKEN}
    return token, index + 1


def read_multiplication(line, index):
    token = {"type": MULT_TOKEN}
    return token, index + 1


def read_division(line, index):
    token = {"type": DIV_TOKEN}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            token, index = read_number(line, index)
        elif line[index] == "+":
            token, index = read_plus(line, index)
        elif line[index] == "-":
            token, index = read_minus(line, index)
        elif line[index] == "*":
            token, index = read_multiplication(line, index)
        elif line[index] == "/":
            token, index = read_division(line, index)
        else:
            print("Invalid character found: " + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):
    tokens.insert(0, {"type": PLUS_TOKEN})
    tokens = calculate_multi_div(tokens)
    print(tokens)
    answer = evaluate_plus_minus(tokens)
    return answer


def evaluate_plus_minus(tokens):
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "NUMBER":
            operator = tokens[index - 1]["type"]
            num = tokens[index]["number"]
            if operator == PLUS_TOKEN:
                answer += num
            elif operator == MINUS_TOKEN:
                answer -= num
            else:
                print("Invalid syntax")
                exit(1)
        index += 1
    return answer


def calculate_multi_div(tokens):
    index = 0
    while index < len(tokens):
        operator = tokens[index - 1]["type"]
        if tokens[index]["type"] == "NUMBER" and (
            operator == MULT_TOKEN or operator == DIV_TOKEN
        ):
            first_number = tokens[index - 2]["number"]
            second_number = tokens[index]["number"]

            if operator == MULT_TOKEN:
                tokens[index - 2]["number"] = first_number * second_number
            elif operator == DIV_TOKEN:
                tokens[index - 2]["number"] = first_number / second_number
            else:
                print("Invalid syntax")
                exit(1)
            tokens.pop(index - 1)
            tokens.pop(index - 1)
        index += 1
    return tokens


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


def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")

    test("11111111+11111111")
    test("11111111-11111111")
    test("1.000-3.99999")
    test("1-2+3-5")

    test("1-2+3-5*0")
    test("15-2+3-5/5")
    test("5/5")
    test("2*3")
    test("3*2")

    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
