import random, sys

###########################################################################
#                                                                         #
# Implement a cache that stores the most recently accessed items from     #
# scratch!                                                                #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################


class Page:
    def __init__(self, url, contents, next, older_url, newer_url):
        # URL
        self.url = url
        # The contents of the URL
        self.contents = contents
        # Previous page
        self.prev = None
        # Next page
        self.next = next
        self.older_url = older_url
        self.newer_url = newer_url


def calculate_hash(key):
    assert type(key) == str
    hash = 0
    for i, c in enumerate(key):
        hash += ord(c) * (i**10)
    return hash


class Cache:
    # Initialize the cache.
    # 'limit': The size limit of the cache.
    def __init__(self, limit):
        assert limit >= 1
        self.limit = limit
        self.hit_count = 0  # Increment on a cache hit
        self.miss_count = 0  # Increment on a cache miss
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        self.oldest_url = None
        self.newest_url = None
        self.buckets = [None] * self.limit
        self.item_count = 0
        # ------------------------#
        # Write your code here!  #
        # ------------------------#

        pass

    # Access a page and update the cache so that it stores the most recently
    # accessed pages up to the 'limit'. This needs to be done with mostly O(1).
    # 'url': The accessed URL
    # 'contents': The contents of the URL
    def access_page(self, url, contents):
        assert type(url) == str

        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        # 削除フェーズ
        # すでにキャッシュにあるならtargetを削除、ないかつsizeがlimitならoldestを削除
        if self.newest_url == url:
            self.hit_count += 1
            return

        if self.remove_target_if_exist(url):
            self.hit_count += 1
            self.item_count -= 1
        else:
            self.miss_count += 1
            print(f"limit:{self.limit} item_count:{self.item_count}")
            if self.item_count == self.limit:
                self.remove_oldest()
                self.item_count -= 1

        # 追加フェーズ
        index = calculate_hash(url) % self.limit
        page = Page(url, contents, self.buckets[index], self.newest_url, None)
        self.buckets[index] = page
        self.item_count += 1

        if not self.oldest_url:
            self.oldest_url = url
        if self.newest_url:
            second_newest_page = self.get_page(self.newest_url)
            second_newest_page.newer_url = url
        self.newest_url = url

        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#

        pages = []
        if not self.newest_url:
            return pages
        current_page = self.get_page(self.newest_url)
        while current_page:
            self.print_page(current_page)
            pages.append(current_page.url)
            if current_page.url == self.oldest_url:
                print(f"get_pages called oldest:url{self.oldest_url}, pages:{pages}")
                return pages
            current_page = self.get_page(current_page.older_url)
        print(f"get_pages called oldest:url{self.oldest_url}, pages:{pages}")
        return pages

    def remove_target(self, url):
        index = calculate_hash(url) % self.limit
        current_page = self.buckets[index]
        if current_page.url == url:
            self.buckets[index] = current_page.next
            return

        prev_item = current_page
        current_page = current_page.next
        while current_page:
            if current_page.url == url:
                prev_item.next = current_page.next
                return True
            prev_item = current_page
            current_page = current_page.next

    def remove_target_if_exist(self, url):
        if url == self.oldest_url:
            self.remove_oldest()
            return True

        target_page = self.get_page(url)
        if not target_page:
            return False

        self.update_relation(target_page.newer_url, None, target_page.older_url)
        self.update_relation(target_page.older_url, target_page.newer_url, None)
        self.remove_target(url)
        return True

    def remove_oldest(self):
        oldest_page = self.get_page(self.oldest_url)
        self.oldest_url = oldest_page.newer_url
        print(f"updated_oldest now:{self.oldest_url} from prev:{oldest_page.url}")
        return

    def get_page(self, url):
        index = calculate_hash(url) % self.limit
        current_page = self.buckets[index]
        while current_page:
            if current_page.url == url:
                return current_page
            current_page = current_page.next
        return None

    def update_relation(self, url, newer_url, older_url):
        index = calculate_hash(url) % self.limit
        current_page = self.buckets[index]
        while current_page:
            if current_page.url == url:
                if newer_url:
                    current_page.newer_url = newer_url
                if older_url:
                    current_page.older_url = older_url
                return
            current_page = current_page.next
        return

    # Return the cache hit rate.
    def get_hitrate(self):
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0

    def print_page(self, page):
        return
        print(f"url:{page.url} newer:{page.newer_url}, older:{page.older_url}")
        print(f"oldest:{self.oldest_url} newest:{self.newest_url}")


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (new)<-- "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (new)<-- "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (new)<-- "d.com", "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (new)<-- "d.com", "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (new)<-- "a.com", "d.com", "c.com", "b.com" -->(old)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (new)<-- "e.com", "a.com", "c.com", "d.com" -->(old)
    print(f"{cache.get_pages()}")
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (new)<-- "f.com", "e.com", "a.com", "c.com" -->(old)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (new)<-- "e.com", "f.com", "a.com", "c.com" -->(old)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (new)<-- "a.com", "e.com", "f.com", "c.com" -->(old)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


def performance_test():
    # Set the size of the cache to 100.
    cache = Cache(100)

    # Generate queries based on the Zipf law.
    ALPHA = 1.5
    NUM_QUERIES = 1000000
    NUM_PAGES = 1000
    ranks = range(1, NUM_PAGES + 1)
    weights = [1.0 / (r**ALPHA) for r in ranks]
    random.seed(1)
    queries = random.choices(ranks, weights=weights, k=NUM_QUERIES)
    for query in queries:
        cache.access_page(str(query), "")

    # If your cache implementation is correct, the hit rate will be 91%.
    print("Cache hit rate = %d %%" % (cache.get_hitrate() * 100))
    print("Performance tests passed!")


if __name__ == "__main__":
    cache_test()
    performance_test()
