"""
@Author  : monabai
@Time    : 2018/7/21 16:29
@Software: PyCharm
@File    : read_data.py
"""
import csv


class ReadData:
    """ """
    def __init__(self):
        pass

    def generate_data(self, file_path):
        if not file_path:
            raise ValueError('YOU MUST SPECIFY THE FILE PATH!')

        # raw_data = []
        with open(file_path, 'r', encoding='utf8') as f:
            if f.readline():  # 去掉第一行的 html 标签
                for line in f:
                    yield line.split(',')[4].strip()  # ID，datetime，rating，helpful，review
            else:
                raise ValueError('empty file: ', file_path)

    def read_database(self, sql):
        pass

    def read_file(self, file_path):

        if not file_path:
            raise ValueError('YOU MUST SPECIFY THE FILE PATH!')

        raw_data = []
        with open(file_path, 'r', encoding='utf8') as f:
            if f.readline():  # 去掉第一行的 html 标签
                for line in csv.reader(f):
                    raw_data.append(line[4].strip())  # ID，datetime，rating，helpful，review
            else:
                raise ValueError('empty file: ', file_path)
        return raw_data


if __name__ == '__main__':
    import time
    start = time.time()
    # attraction_name = '乐山大佛'
    attraction_name = '闻一多纪念馆'
    file_path = './data/data_reviews/' + attraction_name + '.txt'
    # file_path = './data_reviews/bonjour.txt'
    stopwords_file = './data/stopwords/stopwords_marks.txt'
    for i in range(1):
        # print(i)
        rd = ReadData()
        count = 0
        raw_data = rd.read_file(file_path)
        print('raw_data', raw_data)
        print('评论个数: ', len(raw_data))
        print()
        for item in rd.generate_data(file_path):
            count += 1
            print(item)
        print('评论个数: ', count)
        # print(attraction_list)

    print('run time:', time.time() - start)
