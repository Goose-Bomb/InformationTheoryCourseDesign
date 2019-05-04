# @Project : Information Theory Course Design
# @Time    : 2019/5/1
# @Author  : Weng Xiaoran - 2016020902034
# @File    : decoder.py

import numpy as np
from bitarray import bitarray


class CodeTreeNode:
    def __init__(self, left=None, right=None, symbol=None):
        self.left = left
        self.right = right
        self.symbol = symbol


def build_code_tree(code_dict):
    root_node = CodeTreeNode()

    for (symbol, code) in code_dict.items():
        node = root_node
        for bit in code.tolist():
            if bit:
                if node.right == None:
                    node.right = CodeTreeNode()
                node = node.right
            else:
                if node.left == None:
                    node.left = CodeTreeNode()
                node = node.left
        node.symbol = symbol

    return root_node


def decode(data, code_dict):
    decoded = []
    root_node = build_code_tree(code_dict)
    node = root_node

    for bit in data.tolist():
        if bit:
            node = node.right
        else:
            node = node.left

        if node.symbol != None:
            decoded.append(node.symbol)
            node = root_node

    return decoded