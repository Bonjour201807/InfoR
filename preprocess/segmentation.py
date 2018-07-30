import jieba
import jieba.posseg as posseg

# 添加用户自定义词典
jieba.load_userdict('./data/user_dicts/dict_attraction.txt')
jieba.load_userdict('./data/user_dicts/dict_food.txt')
jieba.load_userdict('./data/user_dicts/diming_dict.txt')
jieba.load_userdict('./data/user_dicts/meishi_dict.txt')


class WordSegmentation:
    """ """
    def __init__(self):
        pass

    def seg(self, docs):
        data = []
        for doc in docs:
            data.append([x for x in jieba.cut(doc)])  # 精确模式
        return data

    def seg_pos(self, docs):
        data_pos = []
        for doc in docs:
            data_pos.append([x for x in posseg.cut(doc)])  # 获取词性
        return data_pos


if __name__ == '__main__':
    import time
    start = time.time()
    # raw_data = ['闻一多为湖北浠水县人，著名爱国人士']
    raw_data = ['闻一多为湖北浠水县人，著名爱国人士',
                '我在实高读书的时候去过好几回，不要门票，又近，那时候周末叫上胡季春，涂文涛，余翔，我们几个就一起去里面玩，看看充满文化气息的古物，读读秀丽典雅的古文，也是别有风味。']
    for i in range(1):
        # print(i)
        ws = WordSegmentation()
        data = ws.seg(raw_data)
        data_pos = ws.seg_pos(raw_data)

    print('run time:', time.time() - start)

    # with open('./data/data_output/'+attraction_name+'_seg.txt', 'w') as f:
    #     csv.writer(f).writerows(data)
    # with open('./data/data_output/'+attraction_name+'_posseg.txt', 'w') as f:
    #     csv.writer(f).writerows(data_pos)
    print(data)
    print(data_pos)
    print()
    # for reviews in data_pos:
    #     print([(x.word, x.flag) for x in reviews])
