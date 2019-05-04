# @Project : Information Theory Course Design
# @Time    : 2019/4/19
# @Author  : Weng Xiaoran - 2016020902034
# @File    : run.py
# @Drivel  : Python🐮🍺!

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from bitarray import bitarray

import text_processor
import statistics_analyzer as analyzer
import encoder
import decoder

TEXT_FILENAME = 'texts/' + 'Verbal Advantage Preface.txt'

path = Path(TEXT_FILENAME)
# in case the file is gugugu-ing
if not path.exists():
    print('File: "%s" does not exist!\n' % TEXT_FILENAME)
    exit(-1)

with open(TEXT_FILENAME, 'r') as f:
    text = text_processor.filter_text(f.read())

pmf1 = analyzer.get_first_order_pmf(text)
pmf2 = analyzer.get_second_order_pmf(text)
pmf3 = analyzer.get_third_order_pmf(text)

# calculate entropy
print('[Information Entropy]')
# H1 = H(X)
h1 = -np.sum(pmf1 * np.log2(pmf1))
print('1st-Order entropy: %.6f' % h1)
# H2 = H(X1, X2) / 2
pmf2_flat = pmf2[np.nonzero(pmf2)]
h2 = -np.sum(pmf2_flat * np.log2(pmf2_flat)) / 2
print('2nd-Order entropy: %.6f' % h2)
# H3 = H(X1, X2, X3) / 3
pmf3_flat = pmf3[np.nonzero(pmf3)]
h3 = -np.sum(pmf3_flat * np.log2(pmf3_flat)) / 3
print('3rd-Order entropy: %.6f' % h3)

# # huffman encoding
# [encoded_data_huffman, code_dict_huffman, l_avg_huffman] \
# = encoder.huffman_encode(text, pmf1)
# eff_huffman = h1 / l_avg_huffman

# print('[Huffman coding]')
# print('Average code length: %.5f, Efficiency: %.2f%%' %
#       (l_avg_huffman, eff_huffman * 100.0))

# # shannon encoding
# [encoded_data_shannon, code_dict_shannon, l_avg_shannon] \
# = encoder.shannon_encode(text, pmf1)
# eff_shannon = h1 / l_avg_shannon

# print('[Shannon coding]')
# print('Average code length: %.5f, Efficiency: %.2f%%' %
#       (l_avg_shannon, eff_shannon * 100.0))

# fano encoding
[encoded_data_fano, code_dict_fano, l_avg_fano] \
= encoder.fano_encode(text, pmf1)
eff_fano = h1 / l_avg_fano

print('[Fano coding]')
print('Average code length: %.5f, Efficiency: %.2f%%' %
      (l_avg_fano, eff_fano * 100.0))

for (symbol, code) in code_dict_fano.items():
    print('Symbol:[%c], Code:[%s]' % (symbol, code.to01()))


# decode to original text
# text_d = encoded_data_huffman.decode(code_dict_huffman)
# text_d = encoded_data_shannon.decode(code_dict_shannon)
text_d = decoder.decode(encoded_data_fano, code_dict_fano)
print(''.join(text_d))

print('Original Text Length: %d' % len(text))
print('Decoded Text Length: %d' % len(text_d))
print('Matched: %r' % (text == text_d))

# plot 1st-order PMF
fig1 = plt.figure()

t = np.arange(len(text_processor.ALL_LETTERS))
plt.bar(t, pmf1)
plt.xticks(t, text_processor.ALL_LETTERS)
plt.title('1st-Order PMF')

# plot 2nd-order PMF
fig2 = plt.figure()
plt.imshow(pmf2, cmap=plt.get_cmap('hot'))
plt.title('2nd-Order PMF')

plt.xticks(t, text_processor.ALL_LETTERS)
plt.yticks(t, text_processor.ALL_LETTERS)

plt.show()