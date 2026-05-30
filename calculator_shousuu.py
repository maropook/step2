while True:
    print("> ", end="")
    line = input()
    answer = 0.0
    i = 0
    is_plus = True
    is_period = False
    period_stack = []

    while i < len(line):
        # → 数字を足すのではなくて数字を出すようにしてもらう
        # current_number を持たせる
        # +とかがでてきたらindexを増やす+計算する
        if line[i].isdigit():
            number = 0
            while i < len(line) and line[i].isdigit():
                number = number * 10 + int(line[i])
                i += 1
            if i < len(line) and line[i] == ".":
                keta = 0
                i += 1
                while i < len(line) and line[i].isdigit():
                    number = number * 10 + int(line[i])
                    i += 1
                    keta += 1
                # number /= 10 ** (keta)
                number *= 0.1 ** (keta)
            if is_plus:
                answer += number
                print(f"isplusans:{answer}")
            else:
                answer -= number
        elif line[i] == "+":
            i += 1
            is_plus = True
        elif line[i] == "-":
            i += 1
            is_plus = False
        else:
            print("Invalid character found: " + line[i])
            exit(1)

    print(f"answer = {answer}")
