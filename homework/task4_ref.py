import sys
from collections import deque


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file, encoding="utf-8") as file:
            for line in file:
                id, title = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
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
        # ------------------------#
        # Write your code here!  #
        # ------------------------#

        queue = deque()
        find = 0
        for id, title in self.titles.items():
            if title == start:  # startをページ名 -> id に変換
                start_id = id
                find += 1
            if title == goal:  # goalをページ名 -> id に変換
                goal_id = id
                find += 1
            if find == 2:  # startもgoalもidに変換出来たらbreak
                break
        visited = {}  # 訪問済みページ（現在のページ, 親ページ）
        visited[start_id] = None  # startページは親ページなし
        path = []  # 最短経路
        queue.append(start_id)  # startをキューの末尾に追加
        while queue:
            node = queue.popleft()  # キューの先頭からページを取り出す
            if node == goal_id:  # goalに到達したら、最短経路を辿る
                path.append(goal_id)
                while True:
                    prev = visited[node]
                    path.append(prev)
                    if prev == start_id:
                        break
                    node = prev
                path.reverse()  # 最短経路を逆順にする
                path_title = []
                for id in path:
                    path_title.append(self.titles[id])
                print(path_title)
                return
            for child in self.links[node]:
                if not child in visited:
                    visited[child] = node
                    queue.append(child)  # childをキューの末尾に追加
        pass

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#

        pagerank = {}
        for i in self.titles.keys():  # 全てのページのページランクを１にする
            pagerank[i] = 1.0

        # ページランクの更新
        sum = 1

        while sum >= 0.01:  # 収束条件を満たすまで繰り返す
            old_pagerank = {}  # （ページ名, 古いページランク）
            new_pagerank = {}  # （ページ名, 新しいページランク）

            for i in self.titles.keys():
                old_pagerank[i] = pagerank[i]  # old_pagerank更新

            for i in self.titles.keys():  # ページランク更新
                # 隣接するページがない場合 -> 1.0*pagerank[i]/x を全てのページに加算する（x = 全てのページ数）
                if len(self.links[i]) == 0:
                    for j in self.titles.keys():
                        pagerank[j] += 1.0 * pagerank[i] / len(self.titles)
                    pagerank[i] = 0  # 現在のページのページランク更新

                # 隣接するページがn個ある場合 -> 0.85*pagerank[i]/n を隣接するページに、0.15*pagerank[i] を全てのページに加算する
                # 収束するまで繰り返す　収束条件: Σ(new_pagerank[i] - old_pagerank[i])^2 < 0.01
                else:
                    for j in self.links[i]:  # 隣接するページに0.85*pagerank[i]/nを加算
                        pagerank[j] += 0.85 * pagerank[i] / len(self.links[i])
                    for (
                        j
                    ) in self.titles.keys():  # 全てのページに0.15*pagerank[i]/xを加算
                        pagerank[j] += 0.15 * pagerank[i] / len(self.titles)
                    pagerank[i] = 0  # 現在のページのページランク更新

            for j in self.titles.keys():  # new_pagerankを更新
                new_pagerank[j] = pagerank[j]

            sum = 0  # 収束条件を計算：Σ(new_pagerank[i] - old_pagerank[i])^2
            for j in self.titles.keys():  # 収束条件を計算
                sum += (new_pagerank[j] - old_pagerank[j]) ** 2

        # new_pagerankをページランクについて降順にソートする
        sorted_pagerank = sorted(new_pagerank.items(), reverse=True, key=lambda x: x[1])

        # 上位10個のページ名を出力
        for id, pagerank in sorted_pagerank[:10]:
            print(f"{self.titles[id]} {pagerank}")

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
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()

    # Homework #1
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
