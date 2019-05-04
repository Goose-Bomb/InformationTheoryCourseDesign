from bitarray import bitarray
import numpy as np
import heapq
import decoder

pmf = [0.01, 0.10, 0.15, 0.17, 0.18, 0.19, 0.20]
symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

code_dict = {c: bitarray() for c in symbols}


class HuffmanNode:
    def __init__(self, freq=None, left=None, right=None, symbol=None):
        self.freq = freq
        self.left = left
        self.right = right
        self.symbol = symbol

    def __lt__(self, other):
        return self.freq < other.freq

    def __str__(self):
        return "symbol = %c, freq = %.2f" % (self.symbol, self.freq)


minheap = []

for [p, c] in zip(pmf, symbols):
    leaf_node = HuffmanNode(p, symbol=c)
    heapq.heappush(minheap, leaf_node)

while len(minheap) > 1:
    left_child = heapq.heappop(minheap)
    right_child = heapq.heappop(minheap)

    merged_freq = left_child.freq + right_child.freq
    parent = HuffmanNode(merged_freq, left_child, right_child)
    heapq.heappush(minheap, parent)


def traverse(node, code=bitarray()):
    c = node.symbol
    if c != None:
        code_dict[c] = code
    else:
        traverse(node.left, code + bitarray('1'))
        traverse(node.right, code + bitarray('0'))


traverse(minheap[0])
print(code_dict)

for bit in code_dict['A'].tolist():
    print(bit)

a = "ABCDEFGA"
data = bitarray()
data.encode(code_dict, a)

b = decoder.decode(data, code_dict)
print(b)
