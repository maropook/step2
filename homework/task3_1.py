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
    answer = 0
    tokens.insert(0, {"type": PLUS_TOKEN})
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "NUMBER":
            operator = tokens[index - 1]["type"]
            num = tokens[index]["number"]

            if operator == PLUS_TOKEN:
                answer += num
            elif operator == MINUS_TOKEN:
                answer -= num
            elif operator == MULT_TOKEN:
                answer *= num
            elif operator == DIV_TOKEN:
                if num == 0.0 or num == 0:
                    answer = -float("inf")
                else:
                    answer /= num
            else:
                print("Invalid syntax")
                exit(1)
        index += 1
    return answer


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

    # test("1-2+3-5*0")
    # test("1-2+3-5/0")

    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
