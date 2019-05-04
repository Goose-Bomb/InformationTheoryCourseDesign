# @Project : Information Theory Course Design
# @Time    : 2019/4/25
# @Author  : Weng Xiaoran - 2016020902034
# @File    : encoder.py

import heapq

import numpy as np
from bitarray import bitarray

import text_processor


def shannon_encode(text, pmf1):
    # calculate cumulative probabilities
    cdf = np.insert(np.cumsum(pmf1), 0, 0.0)
    # calculate self-information for each symbol
    i = -np.log2(pmf1)
    # determine code length
    l = np.ceil(i).astype(int)

    # calculate average code length
    l_avg = np.sum(l * pmf1)

    # generate code table
    code_dict = dict.fromkeys(text_processor.ALL_LETTERS)

    def get_binary_fractions(val, length):
        for _i in range(length):
            val = val * 2.0
            if val >= 1.0:
                val = val - 1.0
                yield True
            else:
                yield False

    for c in code_dict.keys():
        i = text_processor.get_index(c)
        code_dict[c] = bitarray(get_binary_fractions(cdf[i], l[i]))

    # encode data using derived code table
    encoding_stream = bitarray()
    encoding_stream.encode(code_dict, text)

    # return encoded data and code table
    return encoding_stream, code_dict, l_avg


def fano_encode(text, pmf1):
    sort_index = np.argsort(pmf1)
    pmf_sorted = pmf1[sort_index]
    symbols_sorted = np.array(text_processor.ALL_LETTERS)[sort_index]

    # generate code table
    code_dict = {symbol: bitarray() for symbol in text_processor.ALL_LETTERS}

    def bisect(s, e):
        # end of recursive
        if s == e - 1: return

        # find dividing position
        m = e
        p_sum = 0.0
        p_delta = 1.0
        p_threshold = sum(pmf_sorted[s:e]) * 0.5

        while m > s:
            p_sum += pmf_sorted[m - 1]
            p_delta_latest = abs(p_sum - p_threshold)
            if p_delta_latest > p_delta: break
            p_delta = p_delta_latest
            m -= 1

        # assign code bit
        # left part -> 1
        for i in range(s, m):
            code_dict[symbols_sorted[i]].append(True)
        # right part -> 0
        for i in range(m, e):
            code_dict[symbols_sorted[i]].append(False)

        # recursive
        bisect(s, m)
        bisect(m, e)

    bisect(0, len(pmf1))

    # calculate average code length
    l = np.fromiter(map(lambda code: len(code), code_dict.values()), float)
    l_avg = np.sum(l * pmf1)

    # encode data using derived code table
    encoding_stream = bitarray()
    encoding_stream.encode(code_dict, text)

    # return encoded data and code table
    return encoding_stream, code_dict, l_avg


class HuffmanNode:
    def __init__(self, freq=None, left=None, right=None, symbol=None):
        self.freq = freq
        self.left = left
        self.right = right
        self.symbol = symbol

    def __lt__(self, other):
        return self.freq < other.freq


def huffman_encode(text, pmf1):

    minheap = []
    for [p, c] in zip(pmf1, text_processor.ALL_LETTERS):
        leaf_node = HuffmanNode(p, symbol=c)
        heapq.heappush(minheap, leaf_node)

    while len(minheap) > 1:
        left_child = heapq.heappop(minheap)
        right_child = heapq.heappop(minheap)

        merged_freq = left_child.freq + right_child.freq
        parent = HuffmanNode(merged_freq, left_child, right_child)
        heapq.heappush(minheap, parent)

    # generate code table
    code_dict = {symbol: bitarray() for symbol in text_processor.ALL_LETTERS}

    def traverse(node, code=bitarray()):
        c = node.symbol
        if c != None:
            # leaf node found, assign code
            code_dict[c] = code
        else:
            traverse(node.left, code + bitarray('1'))
            traverse(node.right, code + bitarray('0'))

    traverse(minheap[0])

    # calculate average code length
    l = np.fromiter(map(lambda code: len(code), code_dict.values()), float)
    l_avg = np.sum(l * pmf1)

    # encode data using derived code table
    encoding_stream = bitarray()
    encoding_stream.encode(code_dict, text)

    # return encoded data and code table
    return encoding_stream, code_dict, l_avg


    
    
