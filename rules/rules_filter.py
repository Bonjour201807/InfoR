"""
@Author  : monabai
@Time    : 2018/7/21 11:16
@Software: PyCharm
@File    : rules_filter.py
"""


class pos_filter:
    """判断词性序列是否满足设定的条件，如果满足返回True，否则返回False"""

    def __init__(self):
        pass

    def token_refuse(self, word):
        if word[0] == word[1] == word[2]:
            return True
        else:
            return False

    def pos_accept(self, pos_seq):
        if pos_seq[0] in ('a', 'n'):
            return True
        else:
            return False

    def pos_refuse(self, pos_seq):
        if pos_seq[-1] in ('uj', 'a', 'p', 'm', 'ul', 'q') or pos_seq[0] in ('uj', 'm'):
            return True
        else:
            return False

    def pos_pattern_accept(self, pos_seq):
        if pos_seq[0] == 'a' and pos_seq[-1] == 'n':
            return True
        else:
            return False

    def pos_pattern_refuse(self, pos_seq):
        if len(pos_seq) == 2 and pos_seq[-1] == 'v':
            return True
        else:
            return False


if __name__ == '__main__':
    pf = pos_filter()
    test1 = ['a', 'uj', 'm', 'n']
    print(pf.pos_accept(test1))
    test2 = ['uj', 'n']
    print(pf.pos_refuse(test2))
