from nltk.util import ngrams
from collections import defaultdict


class freqPhrase():

    def __init__(self, minCount, threshold, stopwordsFile=False):
        self.minCount = minCount

        self.newWords = set()
        self.threshold = threshold

        self.stoplist = ['\n','-','�','>',' ','�',' ','·','\\',':']

        if stopwordsFile:
            with open(stopwordsFile, encoding='utf8') as f:
                stopwords = [word.strip() for word in f]
            self.stoplist.extend(stopwords)
        else:
            pass

    @classmethod
    def bigram_form(cls, docs):
        return [ngrams(words, 2) for words in docs]

    @classmethod
    def word_bigram_fd(cls, data):

        wfd = defaultdict(list)
        bfd = defaultdict(list)
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
        dict_candidate = defaultdict(list)
        dict_finished = defaultdict(list)
        for words in bfd:
            if bfd[words][0] >= self.minCount and \
                                    bfd[words][0] / min(wfd[words[0]][0], wfd[words[1]][0]) > self.threshold and \
                            words[0] not in self.stoplist and words[1] not in self.stoplist:
                dict_candidate[words] = bfd[words]
        i = 0
        while len(dict_candidate) > 0:
            dict_candidate_new = defaultdict(list)
            # print(dict_candidate)
            for word_pair in dict_candidate:
                candidate_temp = defaultdict(list)
                flag = True

                for index in dict_candidate[word_pair][1:]:
                    if index[-1] + 2 <= len(data[index[0]]):
                        candidate_pair_r = tuple(data[index[0]][index[1]:index[-1] + 2])
                        pair_index = [index[0]]
                        # pair_index_l = pair_index+[tuple(range(index[1] - 1, index[-1] + 1))]
                        pair_index_r = tuple(pair_index+range(index[1], index[-1] + 2))
                        if candidate_pair_r[-1] not in self.stoplist:
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
                    if candidate_temp[word][0] >= self.minCount and \
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
    fw = freqPhrase(minCount=4,threshold=0.4)
    data = []
    data = ['abcdeabcdeabcde','abcdebcdefabcde','abcdecdefgabcde','abcdedefghabcde']
    data = [list(line) for line in data]
    print(data)
    for item in fw.combine2words(data).keys():
        print('###'.join(item))