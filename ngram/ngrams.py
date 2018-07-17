from nltk.util import ngrams
from collections import defaultdict


class FreqPhrase():
    """Extract meaningful phrases with high frequency.

    Attributes:
        min_count: A minimum support count for filtering the phrase.
        threshold: A threshhold of confidence to filter the phrase.
        stopwords_file: A file path if there is a stopwords file, None if not.
    """

    def __init__(self, min_count, threshold, stopwords_file=None):  # 把stopwords_file由false改成了None
        """Inits FreqPhrase with stop_list."""
        self.min_count = min_count
        self.newWords = set()
        self.threshold = threshold

        self.stop_list = ['\n', '-', '?', '>', ' ', '？', ' ', '·', '\\', ':']
        # if not stopwords_file:
        #     raise ValueError('YOU MUST SPECIFY PATH')

        if stopwords_file:
            with open(stopwords_file, encoding='utf8') as f:
                stopwords = [word.strip() for word in f]
            self.stop_list.extend(stopwords)
        else:
            pass

    @classmethod
    def bigram_form(cls, docs):
        """

        :param docs:
        :return: all words and 2-grams in docs
        """

        return [ngrams(words, 2) for words in docs]

    @classmethod
    def word_bigram_fd(cls, data):
        """

        :param data:
        :return:
        """

        # 存储 word 和 phrase 的出现频率、文档及句子中的位置
        wfd = defaultdict(list)  # {'a': [9, (0, 0), (0, 5),...], 'b': [10, (0, 1), (0, 6),...],...}
        bfd = defaultdict(list)  # {('a', 'b'): [9, (0, 0, 1),...], ('b', 'c'): [10, (0, 1, 2)],...}
        bigram_data = cls.bigram_form(data)
        for i, line in enumerate(data):
            for j, word in enumerate(line):
                if word in wfd:
                    wfd[word][0] += 1
                    wfd[word].append((i, j))
                else:
                    wfd[word].append(1)
                    wfd[word].append((i, j))

        for i, line in enumerate(bigram_data):
            for j, word in enumerate(line):
                if word in bfd:
                    bfd[word][0] += 1
                    bfd[word].append((i, j, j + 1))
                else:
                    bfd[word].append(1)
                    bfd[word].append((i, j, j + 1))

        return wfd, bfd

    def combine2words(self, data):
        """

        :param data:
        :return:
        """

        wfd, bfd = self.word_bigram_fd(data)
        dict_candidate = defaultdict(list)
        dict_finished = defaultdict(list)
        for words in bfd:
            # 支持度计数、置信度大于设定的阈值，两个词按置信度大的还是小的来算？？？
            # 2-grams中的两个词都不是停用词，是否应该先判断这个？？？还是应该在分词的时候先去停用词？？？
            # 增加分词模块，在分词的时候去停用词，这里不需要进行停用词判断
            # 停用词设置策略：在分词的时候先去掉一部分停用词，后面根据挖掘结果增加停用词表
            if bfd[words][0] >= self.min_count and \
                    bfd[words][0] / min(wfd[words[0]][0], wfd[words[1]][0]) > self.threshold and \
                    words[0] not in self.stop_list and words[1] not in self.stop_list:
                dict_candidate[words] = bfd[words]
        i = 0
        # 终止条件设置？
        # 判断是否应该向右扩展（目前是根据最小置信度判断，可以增加其他策略）
        # 最后得到的频繁子序列（短语），可以进一步筛选，还可以计算ngram2vec
        # 同时找出 abc 和 abcd，应该保留哪一个？
        # 同时找到 abc 和 bcd，是否可以组合得到 abcd？
        # 第一步信息抽取，结构化，先找频繁子序列，第二步信息分类(设置规则，比如动词+名词的可以认为是耍法)
        # 第三步信息关联，得到事理图谱(哈工大LTP)
        # 除了频繁序列(连续)之外还可以挖掘频繁项集
        while len(dict_candidate) > 0:
            dict_candidate_new = defaultdict(list)
            for word_pair in dict_candidate:
                candidate_temp = defaultdict(list)
                flag = True

                for index in dict_candidate[word_pair][1:]:
                    if index[-1] + 2 <= len(data[index[0]]):
                        candidate_pair_r = tuple(data[index[0]][index[1]:index[-1] + 2])
                        pair_index = [index[0]]
                        # pair_index_l = pair_index+[tuple(range(index[1] - 1, index[-1] + 1))]
                        pair_index_r = tuple(pair_index+list(range(index[1], index[-1] + 2)))
                        if candidate_pair_r[-1] not in self.stop_list:
                            if candidate_pair_r in candidate_temp:
                                # if pair_index_r not in candidate_temp[candidate_pair_r]:
                                candidate_temp[candidate_pair_r][0] += 1
                                candidate_temp[candidate_pair_r].append(tuple(pair_index_r))
                            else:
                                candidate_temp[candidate_pair_r].append(1)
                                candidate_temp[candidate_pair_r].append(tuple(pair_index_r))
                        else:continue
                    else:continue

                for word in candidate_temp:
                    if candidate_temp[word][0] >= self.min_count and \
                            candidate_temp[word][0] / min(dict_candidate[word_pair][0], 
                            wfd[word[-1]][0]) > self.threshold:
                        flag = False
                        dict_candidate_new[word] = candidate_temp[word]

                if flag:
                    dict_finished[word_pair] = dict_candidate[word_pair]
            if i > 10:
                dict_finished = dict(dict_finished.items() + dict_candidate.items())
                return dict_finished
            i += 1
            dict_candidate.clear()
            dict_candidate = dict_candidate_new
        return dict_finished


if __name__ == '__main__':
    fw = FreqPhrase(min_count=4,threshold=0.4)
    data = []
    data = ['abcdeabcdeabcde','abcdebcdefabcde','abcdecdefgabcde','abcdedefghabcde']
    data = [list(line) for line in data]
    print(data)
    for item in fw.combine2words(data).keys():
        print('###'.join(item))
