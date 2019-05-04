# @Project : Information Theory Course Design
# @Time    : 2019/4/20
# @Author  : Weng Xiaoran - 2016020902034
# @File    : text_processor.py

import string

ALL_LETTERS = list(' ' + string.ascii_uppercase)


def filter_text(s):
    # merge blanks
    import re
    s = re.sub(r'\s+', ' ', s).upper()
    # filter out non-English characters
    return list(filter(lambda c: c.isascii() and (c.isalpha() or c == ' '), s))


def get_index(c):
    if c == ' ': return 0
    return ord(c) - ord('A') + 1


def get_letter(i):
    if i == 0: return ' '
    return chr(i + 1 + ord('A'))