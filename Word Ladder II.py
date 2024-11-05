from collections import defaultdict, deque

def find_ladders(beginWord, endWord, wordList):
    if endWord not in wordList:
        return []

    wordList = set(wordList)
    wordList.add(beginWord)
    neighbors = defaultdict(list)
    
    for word in wordList:
        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i+1:]
            neighbors[pattern].append(word)
    
    def bfs(beginWord, endWord):
        queue = deque([(beginWord, [beginWord])])
        visited = set([beginWord])
        found = False
        paths = []
        
        while queue and not found:
            local_visited = set()
            for _ in range(len(queue)):
                word, path = queue.popleft()
                for i in range(len(word)):
                    pattern = word[:i] + '*' + word[i+1:]
                    for neighbor in neighbors[pattern]:
                        if neighbor == endWord:
                            found = True
                            paths.append(path + [endWord])
                        if neighbor not in visited:
                            local_visited.add(neighbor)
                            queue.append((neighbor, path + [neighbor]))
            visited.update(local_visited)
        return paths

    return bfs(beginWord, endWord)
