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

    def get_path_from_goal(self, goal_id, prev_nodes):
        path = [(goal_id, self.titles[goal_id])]
        current_id = goal_id
        while current_id in prev_nodes:
            current_id = prev_nodes[current_id]
            path.append((current_id, self.titles[current_id]))
        return path

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = self.ids[start]
        goal_id = self.ids[goal]
        queue = deque([start_id])
        visited = {}
        prev_nodes = {}

        for i in self.ids.values():
            visited[i] = False
        visited[start_id] = True

        while queue:
            current_node_counts = len(queue)
            for _ in range(current_node_counts):
                current_id = queue.popleft()
                if current_id == goal_id:
                    path = self.get_path_from_goal(goal_id, prev_nodes)
                    distance = len(path) - 1
                    print(
                        f"The distance between {start} and {goal} is {distance}. Path is {path}"
                    )
                    return
                for neighbor_id in self.links[current_id]:
                    if not visited[neighbor_id]:
                        prev_nodes[neighbor_id] = current_id
                        queue.append(neighbor_id)
                        visited[neighbor_id] = True
        print("Start and goal is not connected")
        return

    # 上位nthのpage_rankをlistで返す、O(N*n)オーダー
    def find_highest_nth_pages(self, n, page_rank_dict):
        page_ranks = list(page_rank_dict.items())
        ans = []
        for _ in range(min(len(page_ranks), n)):
            ith_highest = -1
            ith_highest_pos = -1
            for j in range(len(page_ranks)):
                if ith_highest < page_ranks[j][1]:
                    ith_highest = page_ranks[j][1]
                    ith_highest_pos = j
            current = page_ranks.pop(ith_highest_pos)
            ans.append(current)
        return ans

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        new_pagerank = {}
        old_pagerank = {}

        diff = 1.0
        N = len(self.ids)

        for i in self.ids.values():
            new_pagerank[i] = 1.0

        while diff > 0.01:
            old_pagerank = new_pagerank.copy()
            new_pagerank = {}
            page_rank_for_all = 0.0

            # 全てのnodeからつながっている全てのnodeに対してpage_rank_for_connectedを配る
            for old_id, rank in old_pagerank.items():
                neighbors = self.links[old_id]
                connected_counts = len(neighbors)

                if connected_counts == 0:
                    page_rank_for_all += rank
                    page_rank_for_connected = 0.0
                else:
                    page_rank_for_all += rank * 0.15
                    page_rank_for_connected = (rank * 0.85) / float(connected_counts)
                    for n_id in neighbors:
                        if n_id not in new_pagerank:
                            new_pagerank[n_id] = page_rank_for_connected
                        else:
                            new_pagerank[n_id] += page_rank_for_connected

            # 全てのnodeにpage_rank_for_allを配る
            for i in self.ids.values():
                if i not in new_pagerank:
                    new_pagerank[i] = page_rank_for_all / float(N)
                else:
                    new_pagerank[i] += page_rank_for_all / float(N)

            # 1回のループでどれぐらいの大きさ更新されたかと全てのpage_rankの合計を計算する
            diff = 0
            current_sum = 0
            for i in self.ids.values():
                diff += (new_pagerank[i] - old_pagerank[i]) ** 2
                current_sum += new_pagerank[i]
            assert abs(current_sum - N) < 1e-4

        # 上位10個のpage_rankを取得する(O(N*上位n))
        highest_tenth_pages = self.find_highest_nth_pages(10, new_pagerank)
        for page_rank in highest_tenth_pages:
            print(f"Title:{self.titles[page_rank[0]]}, Page_rank:{page_rank[1]}")
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
    # wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    # wikipedia.find_longest_path("渋谷", "池袋")
