import sys
from collections import deque


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        self.titles = {}
        self.ids = {}
        self.links = {}
        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                id, title = line.rstrip().split(" ")
                id = int(id)
                assert id not in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                src, dst = line.rstrip().split(" ")
                src, dst = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

        for key, value in self.titles.items():
            self.ids[value] = key

    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        distance = -1
        start_id = self.ids[start]
        goal_id = self.ids[goal]
        # index = ID
        visited = {}
        for i in self.ids.values():
            visited[i] = False
        visited[start_id] = True

        queue = deque([(start_id, [])])
        distance = 0
        while queue:
            current_node_counts = len(queue)
            for _ in range(current_node_counts):
                current = queue.popleft()
                current_id, path = current[0], current[1]
                if current_id == goal_id:
                    print(
                        f"The distance between {start} and {goal} is {distance}. Path is {path}"
                    )
                    return

                for neighbor in self.links[current_id]:
                    current_path = path[:]
                    current_path.append(current_id)
                    if not visited[neighbor]:
                        queue.append((neighbor, current_path))
                        visited[neighbor] = True
            distance += 1
        print("start and goal is not connected")
        return

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        # 宿題2
        # find_most_popular_pages() 関数を書いて、ページランクを計算して重要度の高いページトップ 10 を求めてください
        # このスライドで「言葉で説明したアルゴリズムを自分で具体化してコードに落とす」のが宿題の意図です
        # 50 行程度で書けます 😀
        # ヒント
        # 正しさの確認方法
        # ページランクの分配と更新を何回繰り返しても「全部のノードのページランクの合計値」が一定に保たれることを確認してください
        # 一定にならない場合何かが間違ってます！
        # Large のデータセットで動かすためには O(N + E) のアルゴリズムが必要です
        # ページ数：N = 2215900
        # リンク数：E = 119006494
        # ページランクの更新が「完全に」収束するのは時間がかかりすぎるので、更新が十分少なくなったら止める
        # 収束条件の作り方の例：
        # ∑(new_pagerank[i] - old_pagerank[i])^2 < 0.01
        # pagelankの計算はindex0からlinkしているものたちにpagelank_conected =( 0.85 * connected) len(connectedd),  pagelank_all = (0.15 * current)/len(all)
        # 最後の一周でallのやつを全てのindexに対して足していく
        # for文で∑(new_pagerank[i] - old_pagerank[i])^2 < 0.01
        # new_pagerankとold_pagerankをちょくちょく作っていく
        pass

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass

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
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    # wikipedia.find_longest_titles()
    # # Example
    # wikipedia.find_most_linked_pages()

    # Homework #1
    wikipedia.find_shortest_path("渋谷", "小野妹子")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
