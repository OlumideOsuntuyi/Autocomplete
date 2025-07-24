import pickle
from collections import deque

def get_index(char):
    return ord(char) - ord('a')

def load_lines_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        _lines = file.read().split('\n')
    return _lines

class Node:
    def __init__(self, alphabet, depth):
        self.alphabet = alphabet
        self.depth = depth
        self.count = 0
        self.bias = 0
        self.next_words = 0
        self.branches:dict[str, Node] = {}

    def push(self, queue):
        if len(queue) == 0:
            return # quit node branching
        q = queue.popleft()
        if q not in self.branches:
            self.branches[q] = Node(q, self.depth + 1)

        self.branches[q].push(queue) # next recursion


    def get_count(self):
        _sum = 0
        for node in self.branches.values():
            _sum += node.get_count()
        self.count = _sum # recursive counting
        return self.count

    def get_top_n_nodes(self, n:int):
        # Sort by Node.count descending and return top N (as list of (key, Node) tuples)
        return sorted(
            self.branches.items(),
            key=lambda item: item[1].count,
            reverse=True
        )[:n]

    def word(self, prev:str="", exclusion_list:list[str]=None):
        w = prev + self.alphabet
        sorted_branches = self.get_top_n_nodes(len(self.branches))
        for _, br in sorted_branches:
            r = br.word(w, exclusion_list)
            if not exclusion_list or r not in exclusion_list:
                return r
        return w


    def words(self, prev:str="", count=3):
        _words = []
        i = 0
        MAX_TRIES = 64
        while len(_words) < count and i < MAX_TRIES:
            w = prev + self.alphabet
            tp_nd = self.get_top_n_nodes(count)
            if len(tp_nd) == 0:
                return _words

            for _, nd in tp_nd:
                _w = nd.word(w, _words)
                if _w not in _words:
                    _words.append(_w)

            i += 1
        return _words

    def complete(self, original, queue, count=3):
        if len(self.branches) == 0 or len(queue) == 0:
            return self.words(original, count)

        q = queue.popleft()
        if q not in self.branches:
            return []

        return self.branches[q].complete(original, queue, count)



class WordCompleter:
    def __init__(self):
        self.nodes = {}

    def set(self, _words:list[str], path="autocomplete.pkl"):
        for i, word in enumerate(_words):
            if len(word) == 0:
                continue
            queue = deque(word)
            q = queue.popleft()
            if q not in self.nodes:
                self.nodes[q] = Node(q, 0) # add queue

            self.nodes[q].push(queue) # load queue into node
            if i % 100 == 0: # display
                print(f'{i} of {len(_words)}', end='\r', flush=True)

        for node in self.nodes.values():
            node.get_count()

        self.save(path)

    def complete(self, txt:str, count:int):
        _queue = deque(txt)
        q = _queue.popleft()
        _words = self.nodes[q].complete(txt, _queue, count)
        return _words

    def save(self, filepath="autocomplete.pkl"):
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filepath="autocomplete.pkl"):
        with open(filepath, "rb") as f:
            return pickle.load(f)




autocomplete = WordCompleter.load()
#text = load_lines_from_txt('words.txt')
#autocomplete.set(text)

words = autocomplete.complete('ba', 3)
print(words)

