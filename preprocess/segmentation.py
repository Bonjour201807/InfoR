import csv
import jieba


# 添加用户自定义词典
jieba.load_userdict('../../data/user_dicts/dicts_food.txt')

class WordSegmentation:
    """ """
    def __init__(self):
        pass

    def read_data(self, file_path):

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

    def segmentation(self, file_path):
        data = []
        raw_data = self.read_data(file_path)
        for item in raw_data:
            data.append([x for x in jieba.cut(item)])  # 使用精确模式
        return data


if __name__ == '__main__':
    import time
    start = time.time()
    attraction_name = '乐山大佛'
    file_path = '../../data/data_reviews/' + attraction_name + '.txt'
    # file_path = '../../data_reviews/bonjour.txt'
    stopwords_file = '../../data/stopwords/stopwords_marks.txt'
    for i in range(1):
        # print(i)
        ws = WordSegmentation()
        raw_data = ws.read_data(file_path)
        # print('评论个数: ', len(raw_data))
        # print(attraction_list)
        data = ws.segmentation(file_path)

    print('run time:', time.time() - start)
    # print(data)
