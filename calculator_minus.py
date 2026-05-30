while True:
    print("> ", end="")
    line = input()
    answer = 0
    i = 0
    isPlus = True
    while i < len(line):
        # → 数字を足すのではなくて数字を出すようにしてもらう
        # current_number を持たせる
        # +とかがでてきたらindexを増やす+計算する
        if line[i].isdigit():
            number = 0
            while i < len(line) and line[i].isdigit():
                number = number * 10 + int(line[i])
                i += 1
            if isPlus:
                answer += number
            else:
                answer -= number
        elif line[i] == "+":
            i += 1
            isPlus = True
        elif line[i] == "-":
            i += 1
            isPlus = False
        else:
            print("Invalid character found: " + line[i])
            exit(1)
    print("answer = %d\n" % answer)
