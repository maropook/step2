def dfs(start, goal):
    stack = Stack()
    stack.push(start)
    seen = [start]
    while not stack.empty():
        node = stack.pop()
        if node == goal:
            return
        for child in links[node]:
		 if child not in seen:
            	stack.push(child)
		     seen.append(child)


