from nltk.util import ngrams
from collections import defaultdict


class FreqPhrase:
    """ Extract meaningful phrases with high frequency.

        Attributes:
            min_count: A minimum support count for filtering the phrase.
            threshold: A threshhold of confidence to filter the phrase.
    """

    def __init__(self, min_count, threshold, stopwords_file=None):
        self.min_count = min_count

        self.newWords = set()
        self.threshold = threshold

        # self.stoplist = ['\n','-','�','>',' ','�',' ','·','\\',':']
        self.stoplist = [' ']

        if stopwords_file:
            with open(stopwords_file, encoding='utf8') as f:
                stopwords = [word.strip() for word in f]
            self.stoplist.extend(stopwords)
        else:
            pass

    @classmethod
    def bigram_form(cls, docs):
        return [ngrams(words, 2) for words in docs]

    @classmethod
    def word_bigram_fd(cls, data):

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
        wfd, bfd = self.word_bigram_fd(data)
        # print('data: ', data)
        # print('wfd: ', wfd)
        # print('bfd: ', bfd)
        dict_candidate = defaultdict(list)
        dict_finished = defaultdict(list)
        for words in bfd:
            if words[0] not in self.stoplist and words[1] not in self.stoplist:
                if bfd[words][0] >= self.min_count and \
                        bfd[words][0] / min(wfd[words[0]][0], wfd[words[1]][0]) > self.threshold:
                    dict_candidate[words] = bfd[words]

        dict_finished.update(dict_candidate)
        i = 0
        while len(dict_candidate) > 0:
            # print('dict_candidate: ', dict_candidate)
            dict_candidate_new = defaultdict(list)
            for word_pair in dict_candidate:
                # print('for word_pair in dict_candidate:', word_pair)
                candidate_extend = defaultdict(list)
                # flag = True

                # positions 是一个三元组，记录了word_pair在第几篇文档中，以及在文档中的起始位置和结束位置
                for positions in dict_candidate[word_pair][1:]:
                    if positions[-1] + 2 <= len(data[positions[0]]):
                        candidate_pair_r = tuple(data[positions[0]][positions[1]:positions[-1] + 2])
                        pair_positions = [positions[0]]
                        pair_positions_r = tuple(pair_positions+list(range(positions[1], positions[-1] + 2)))
                        if candidate_pair_r[-1] not in self.stoplist:
                            if candidate_pair_r in candidate_extend:
                                candidate_extend[candidate_pair_r][0] += 1
                                candidate_extend[candidate_pair_r].append(tuple(pair_positions_r))
                            else:
                                candidate_extend[candidate_pair_r].append(1)
                                candidate_extend[candidate_pair_r].append(tuple(pair_positions_r))
                        else:
                            continue
                    else:
                        continue

                for word in candidate_extend:
                    # print('for word in candidate_extend', word)
                    if candidate_extend[word][0] >= self.min_count and \
                            candidate_extend[word][0] / min(dict_candidate[word_pair][0], wfd[word[-1]][0]) > self.threshold:
                        # flag = False
                        dict_candidate_new[word] = candidate_extend[word]

                # if flag:
                #     dict_finished[word_pair] = dict_candidate[word_pair]
                #     print('dict_finished', dict_finished)

            # if i == 1:
            #     # dict_finished = dict(dict_finished.items() + dict_candidate.items())
            #     dict_finished.update(dict_candidate)
            #     return dict_finished
            i += 1
            dict_candidate.clear()
            dict_candidate = dict_candidate_new
            dict_finished.update(dict_candidate)
        return dict_finished


if __name__ == '__main__':
    stopwords_file = './data/stopwords/stopwords_marks.txt'
    fw = FreqPhrase(min_count=1, threshold=0, stopwords_file=stopwords_file)
    data = []  # data 必须是 list 格式，不然 ngrams 返回值为空
    # data = ['abcdeabcdeabcde', 'abcdebcdefabcde', 'abcdecdefgabcde', 'abcdedefghabcde']
    # data = [list(line) for line in data]
    data = [['闻一多', '为', '湖北', '浠水县', '人', '，', '著名', '爱国人士']]
    # data = [['闻一多', '为', '湖北', '浠水县', '人', '，', '著名', '爱国人士'],
    #         ['我', '在', '实高', '读书', '的', '时候', '去过', '好几回', '，', '不要', '门票', '，', '又', '近', '，',
    #          '那', '时候', '周末', '叫', '上', '胡', '季春', '，', '涂文涛', '，', '余翔', '，', '我们', '几个', '就',
    #          '一起', '去', '里面', '玩', '，', '看看', '充满', '文化', '气息', '的', '古物', '，', '读读', '秀丽', '典雅',
    #          '的', '古文', '，', '也', '是', '别有风味', '。']]
    print(data)
    count = 0
    for item in fw.combine2words(data).keys():
        count += 1
        print('###'.join(item))

    print('频繁子序列的个数：', count)
