# @Project : Information Theory Course Design
# @Time    : 2019/4/19
# @Author  : Weng Xiaoran - 2016020902034
# @File    : statistics_analyzer.py

import numpy as np

import text_processor


def get_first_order_pmf(text):
    # select valid characters and map to ascii
    mapped_index = map(text_processor.get_index, text)

    pmf1 = np.zeros((27))
    # count letters
    for i in mapped_index:
        pmf1[i] = pmf1[i] + 1.0

    # calculate 1st order PMF
    return pmf1 / np.sum(pmf1)


def get_second_order_pmf(text):
    # select valid characters and map to ascii
    mapped_index = list(map(text_processor.get_index, text))

    pmf2 = np.zeros((27, 27))
    # traverse 2-symbol pairs
    for k in range(1, len(mapped_index) - 1):
        i = mapped_index[k - 1]
        j = mapped_index[k]
        pmf2[i, j] = pmf2[i, j] + 1.0

    # calculate 2nd-order PMF
    return pmf2 / np.sum(pmf2)


def get_third_order_pmf(text):
    # select valid characters and map to ascii
    mapped_index = list(map(text_processor.get_index, text))

    pmf3 = np.zeros((27, 27, 27))
    # traverse 3-symbol pairs
    for k in range(2, len(mapped_index) - 1):
        i0 = mapped_index[k - 2]
        i1 = mapped_index[k - 1]
        i2 = mapped_index[k]
        pmf3[i0, i1, i2] = pmf3[i0, i1, i2] + 1.0

    # calculate 3rd-order PMF
    return pmf3 / np.sum(pmf3)
