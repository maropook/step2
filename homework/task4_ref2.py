import sys
from collections import deque

"""
The most linked pages are:
ISBN is linked by 52641 pages

The most popular pages are:
1 : 英語         1507.2977005633572
2 : ISBN         959.7071288949198
3 : 2006年       526.1013566022116
4 : 2005年       502.26093242073915
5 : 2007年       491.4818505921765
6 : 東京都       480.2739485162408
7 : 昭和         459.3758140731063
8 : 2004年       445.3697475755544
9 : 2003年       404.73835956781556
10 : 2000年      401.8895544495601
"""


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # ID -> pade title へのmapping
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # page title -> ID への　mapping
        self.ids = {}

        # ID -> そのページがリンクしているページのIDリスト　へのmapping
        self.links = {}

        # ID -> そのページをリンクしているページのIDリスト　へのmapping
        # リンクを逆向きにたどりたい時につかう
        self.linked = {}

        # ページランクの初期化
        # find_most_popular_pages()で正しいページランクをつける
        self.pageranks = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                id, title = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.ids[title] = id
                self.links[id] = []
                self.linked[id] = []
                self.pageranks[id] = 1.0
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                src, dst = line.rstrip().split(" ")
                src, dst = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
                self.linked[dst].append(src)
        print("Finished reading %s" % links_file)
        print()

    # タイトルの長い上位ｎページを探す。
    def find_longest_titles(self, n):

        # titlesを、長さをキーに降順にソート
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0

        while count < n and index < len(titles):
            if titles[index].find("_") == -1:  # _を使って複数単語並べたものは除く
                print(titles[index])
                count += 1
            index += 1
        print()

    # Example: Find the most linked pages.
    def find_most_linked_pages(self):

        # リンクされているページ数を保存する辞書link_countの初期設定
        link_count = {}

        # 各ページごとにリンクされているページのcountを1増やす
        for id in self.titles.keys():
            link_count[id] = len(self.linked[id])

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(f"{self.titles[dst]} is linked by {link_count_max} pages")
        print()

    # id列からタイトル列に変換する関数
    def id_to_title(self, id_list):
        new_list = []
        for id in id_list:
            new_list.append(self.titles[id])

        return new_list

    # あるページから、ｎステップ内でいける全てのページのタイトルを返す
    def find_pages_in_Nstep(self, page_title, n):
        page_id = self.ids[page_title]
        search = self.links[page_id]

        for i in range(1, n + 1):
            print(f"{i}step from {page_title}")
            new_search = []

            for page in search:
                print(self.titles[page])
                new_search += self.links[page]

            search = new_search
        return

    # startからgoalまでの最短パスをBFS探索で求める
    # 引数start, goalはページタイトル
    # (IDのリストで表されたpath, タイトルのリストで表されたpath, ステップ数)をprintする
    def find_shortest_path(self, start, goal):

        print(f"{start}から{goal}までの最短距離を探索する")

        # ページ同士のリンク管理はタイトルではなくIDで行うので変換しておく
        start_id = self.ids[start]
        goal_id = self.ids[goal]

        if start == goal:
            print(f"IDで表したPath：{[start_id]}")
            print(f"タイトルで表したPath：{[start]}")
            print("ステップ数：0")
            return

        # 探索中のページのidを管理するキュー
        # 初期状態では、startのidのみ入っている
        que = deque([start_id])

        # 探索済みページを管理する辞書。
        # id -> そのページの一個前のページ　のmapping
        # 最後にはこれを逆向きに辿ることでパスを得る
        visited = {}
        visited[start_id] = start_id

        while len(que) > 0:
            page_id = que.popleft()

            for child_id in self.links[page_id]:
                if child_id == goal_id:

                    path = [goal_id, page_id]
                    cur = page_id
                    while True:

                        path.append(visited[cur])
                        cur = visited[cur]

                        if cur == start_id:
                            break

                    path.reverse()

                    # パスとステップ数を表示させる。
                    # pathの要素はIDよりタイトルの方がわかりやすいので変換したものも返す
                    print(f"IDで表したPath：{path}")
                    print(f"タイトルで表したPath：{self.id_to_title(path)}")
                    print(f"ステップ数：{len(path) - 1}")
                    return

                else:
                    # 子ページが未探索であった時、キューに入れる
                    # visited[id]は、一個前のページを指すので、page_id
                    if child_id not in visited:
                        que.append(child_id)
                        visited[child_id] = page_id

        print("Not found")

    # startから、goalまでのパスを、双方向のBFS探索で求める
    # startとgoalの双方向から探索し共通のページに辿り着いたらstart -> 共通のページ -> goalが答え
    def find_shortest_path2(
        self, start, goal
    ):  # 例）start = "渋谷", goal = "小野妹子" -> ["渋谷", "ギャルサー”, "小野妹子"]

        start_id = self.ids[start]
        goal_id = self.ids[goal]

        if start == goal:
            return [start_id], [start], 0

        # キュー、visitedはどちらもstartからの探索用とgoalからの探索用の2つ作る
        q_start = deque([start_id])
        q_goal = deque([goal_id])

        visited_from_start = {}
        visited_from_goal = {}

        visited_from_start[start_id] = start_id
        visited_from_goal[goal_id] = goal_id

        while (len(q_start) > 0) and (len(q_goal) > 0):

            # q_startとq_goalの双方から一つページをpopする
            page_from_start = q_start.popleft()  # 例）"渋谷"
            page_from_goal = q_goal.popleft()  # 例）"小野妹子"

            # startからの探索範囲と、goalからの探索範囲が重なる瞬間を探す
            for child_from_start in self.links[page_from_start]:

                if child_from_start in visited_from_goal:

                    path = [child_from_start, page_from_start]
                    cur = page_from_start

                    # まずはスタートからのパスを逆向きに入れる　→ 反転
                    while True:
                        path.append(visited_from_start[cur])
                        cur = visited_from_start[cur]

                        if cur == start_id:
                            break

                    path.reverse()

                    # その後ゴールからのパスを入れる
                    cur = child_from_start
                    if cur != start_id:
                        while True:
                            path.append(visited_from_goal[cur])
                            cur = visited_from_goal[cur]

                            if cur == goal_id:
                                break

                    print(f"IDで表したPath{path}")
                    print(f"タイトルで表したPath：{self.id_to_title(path)}")
                    print(f"ステップ数：{len(path) - 1}")
                    return

                else:
                    if (
                        child_from_start not in visited_from_start
                    ):  # 例）ここで"ギャルサー"がvisited_from_startに入る
                        q_start.append(child_from_start)
                        visited_from_start[child_from_start] = page_from_start

            for child_from_goal in self.linked[page_from_goal]:

                if child_from_goal in visited_from_start:  # 例）"ギャルサー"が見つかる

                    path = [child_from_goal]
                    cur = child_from_goal

                    # まずはスタートからのパスを逆向きに入れる　→ 反転
                    while True:
                        path.append(visited_from_start[cur])
                        cur = visited_from_start[cur]

                        if cur == start_id:
                            break

                    path.reverse()

                    # その後ゴールからのパスを入れる
                    path.append(page_from_goal)
                    cur = page_from_goal
                    if cur != goal_id:
                        while True:

                            path.append(visited_from_goal[cur])
                            cur = visited_from_goal[cur]

                            if cur == goal_id:
                                break

                    print(f"IDで表したPath{path}")
                    print(f"タイトルで表したPath：{self.id_to_title(path)}")
                    print(f"ステップ数：{len(path) - 1}")
                    return

                else:
                    if child_from_goal not in visited_from_goal:
                        q_goal.append(child_from_goal)
                        visited_from_goal[child_from_goal] = page_from_goal

        print("Not found")

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):

        # 現在持っているページランクの0.85をリンクしている全ページに分けて配る。0.15は全ページに配る
        change = 1
        while change > 0.01:

            # 更新後のページランクを入れるmapping
            new_pageranks = {}

            # 全体に分けるページランクは、一箇所に集めておいて最後に一気に分ける。
            # その都度分けると全体に分けるページランクの計算は計算量O(N^2), 最後にまとめればO(N)
            # アルゴリズム全体で考えるとO (N^2)
            pagerank_forall = 0
            for page_id in self.pageranks:

                # そのページからのリンクが一つ以上ある時
                if len(self.links[page_id]) > 0:

                    # リンクされている一つのページに加えるページランク
                    links_pagerank = (
                        self.pageranks[page_id] * 0.85 / len(self.links[page_id])
                    )

                    # 持っているページランクのうち0.15を全ページに分ける
                    pagerank_forall += (
                        self.pageranks[page_id] * 0.15 / len(self.pageranks)
                    )

                    for link_page in self.links[page_id]:
                        if link_page in new_pageranks:
                            new_pageranks[link_page] += links_pagerank
                        else:
                            new_pageranks[link_page] = links_pagerank

                # そのページからのリンクが一つもない時（末端のページ）、全ページに分ける
                else:
                    pagerank_forall += self.pageranks[page_id] / len(self.pageranks)

            for page_id in self.pageranks:
                if page_id in new_pageranks:
                    new_pageranks[page_id] += pagerank_forall
                else:
                    new_pageranks[page_id] = pagerank_forall

            # 更新による変化分を計算
            change = 0
            for page_id in self.pageranks:

                change += (self.pageranks[page_id] - new_pageranks[page_id]) ** 2

            self.pageranks = new_pageranks

        print("The most popular pages are:")
        # ページランクが大きい順に辞書全体をソート 例：smallの時　{3: 1.373, 4: 1.373, 2: 1.196, 5: 0.811, 6: 0.811, 1: 0.433}
        sorted_pageranks = dict(
            sorted(self.pageranks.items(), key=lambda item: item[1], reverse=True)
        )
        # ページIDが、ページランクの高い順に並んだリストを作る 例：[3, 4, 2, 5, 6, 1]
        pageranks_list = list(sorted_pageranks)
        for i in range(min(10, len(self.pageranks))):
            print(
                f"{i + 1} : {self.titles[pageranks_list[i]]} \t {self.pageranks[pageranks_list[i]]}"
            )

        return

    # Homework #3 (optional):
    # startからgoalまでの、なるべく長い経路を探索し、IDリストで返す。
    # 引数で、使いたくないページIDリストvisitedを指定できる。
    # こうすることで、一つのPathに部分的にこの関数を使う時に便利
    def find_longest_path(self, start, goal, visited_IDs):

        # Pathを30個見つけ、その中で最もパスが長いものを返す
        LIMIT = 30

        # その時に使用する変数countと、今まで見た中で最も長いパスを保存するmost_long_path
        count = 0
        most_long_path = []

        start_id = self.ids[start]
        goal_id = self.ids[goal]

        # スタックを使用して深さ優先探索を行う
        stack = deque()
        stack.append(start_id)

        # 探索済みページを管理する辞書。引数で指定があるときそれを反映させる
        # id -> そのページに到達するまでのパス　のmapping
        visited = {}
        if visited_IDs:
            for visited_pageID in visited_IDs:
                visited[visited_pageID] = True
        visited[start_id] = start_id

        while len(stack) > 0 and count < LIMIT:
            page_id = stack.pop()

            # 先にpage_idまでのパスを辿っておく
            # 逆向きに追加していき、最後に反転
            path_to_pageID = [page_id, visited[page_id]]
            cur = visited[page_id]
            while True:
                path_to_pageID.append(visited[cur])
                cur = visited[cur]

                if cur == start_id:
                    break
            path_to_pageID.reverse()

            # popした親ページpage_idからリンクされている子ページのリストchildren
            children = self.links[page_id]

            # ID -> pageranksのmapping
            childsID_to_pageranks = {}
            for child in children:
                childsID_to_pageranks[child] = self.pageranks[child]

            # ページランクの大きい順にstackからPOPされるように、小さい順に並べる
            sorted_ID_to_pr = dict(
                sorted(childsID_to_pageranks.items(), key=lambda item: item[1])
            )
            children = list(
                sorted_ID_to_pr
            )  # ページIDのみが、ページランク順に並ぶように書き換える

            for child_id in children:
                # goalを見つけた時、pathの正しさをassert_path()で確かめる
                # そしてパスの長さmost_long_pathと比べ, 長ければ更新。countを1増やす
                if child_id == goal_id:

                    found_path = path_to_pageID + [child_id]
                    self.assert_path(found_path, start, goal)
                    if len(found_path) > len(most_long_path):
                        most_long_path = found_path
                    print(f"found {count} : {len(found_path) - 1} steps")
                    count += 1

                else:
                    # visitedに入っていないかではなく、親ページのパスに入っていないかどうかで判定

                    if child_id not in path_to_pageID:
                        # 一度探索されているページの時、現在のパスよりも長いものが見つかった時のみ更新する。
                        if child_id in visited:

                            # visited[child_id] == Trueの時、そもそも到達してはいけないページなので考えない
                            if (visited[child_id] != True) and len(
                                visited[page_id]
                            ) + 1 > len(visited[child_id]):
                                visited[child_id] = page_id
                                # もう一度スタックに入れる
                                stack.append(child_id)
                        else:  # まだ探索されたことのないページの時
                            visited[child_id] = page_id
                            stack.append(child_id)

        return most_long_path

    ### メインの最短距離探索関数 ###
    # この中で、一個上のfind_longest_pathをたくさん呼ぶ。
    # 【方針】
    # 方針:DFS探索において、ページランクが大きいほうに進み続け、30回goalを見つける。
    # そのうち一番長いpathを基準に、もっと長くすることを考える。
    # もっと長くするときの考え方は、各ページとページの間に、もっと長い経路が存在しないか探す。
    def find_longest_path_main(self, start, goal):

        # まずは一個、基準となるPathを作る。
        main_path = self.find_longest_path(start, goal, None)

        # 見つかったステップをさらに長くしていく
        # 見つかったパスが① → ③ → ⑨ → ②ならば、①→③の間に何か他のページを挟むことはできないか？を考える

        index = 0
        while index < len(main_path) - 1:

            # 一度コピーし、main_path[i], main_path[i + 1]を取り除いたリスト作る
            pages_in_path = main_path.copy()
            del pages_in_path[index : index + 2]

            add_path = self.find_longest_path(
                self.titles[main_path[index]],
                self.titles[main_path[index + 1]],
                pages_in_path,
            )
            # LIMIT内でゴールを見つけられず、add_path = []の時はmain_pathを更新しない。
            if add_path != []:
                main_path = main_path[:index] + add_path + main_path[index + 2 :]
            print(len(main_path))
            index += 1

    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert start != goal
        assert len(path) >= 2
        assert self.titles[path[0]] == start
        assert self.titles[path[-1]] == goal
        for i in range(len(path) - 1):
            assert path[i + 1] in self.links[path[i]]
        visited = {}
        for node in path:
            assert node not in visited
            visited[node] = True


if __name__ == "__main__":

    # コマンドライン引数なしで実行 -> 標準入力で番号のみ入力することでサイズを選べる
    # サイズを色々変えて実行する時毎回コマンドライン引数を書き換えるのが面倒なため
    print("select dataset size: \n1: small\n2: medium\n3: large\n")
    n = input()
    if n == "1":
        pages_file = "wikipedia_dataset/pages_small.txt"
        links_file = "wikipedia_dataset/links_small.txt"
    elif n == "2":
        pages_file = "wikipedia_dataset/pages_medium.txt"
        links_file = "wikipedia_dataset/links_medium.txt"
    elif n == "3":
        pages_file = "wikipedia_dataset/pages_large.txt"
        links_file = "wikipedia_dataset/links_large.txt"
    else:
        print("select number (1~3)")
        exit(1)

    # ↓コマンドラインからデータセット指定したい時
    # wikipedia = Wikipedia(sys.argv[1], sys.argv[2])

    wikipedia = Wikipedia(pages_file, links_file)

    wikipedia.find_longest_titles(15)
    wikipedia.find_most_linked_pages()

    # Homework #2
    wikipedia.find_most_popular_pages()

    # Homework #3 (optional)
