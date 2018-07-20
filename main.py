"""
@Author  : monabai
@Time    : 2018/7/18 17:31
@Software: PyCharm
@File    : main.py.py
"""
import os
import time
import csv
from ngram import nrams
from preprocess import segmentation


def test(attraction_name, stopwords_file):
    file_path = '/Users/monabai/Desktop/data/pinglun/' + attraction_name + '.txt'
    # file_path = '../../data/data_reviews/' + attraction_name + '.txt'
    # file_path = '../../data_reviews/bonjour.txt'

    """方法一：不分词，以单个字符为粒度检测频繁子序列，不使用各种标点符号作为分隔符"""
    start = time.time()
    for i in range(1):
        # print(i)
        result = []
        ws = segmentation.WordSegmentation()
        try:
            raw_data = ws.read_data(file_path)
        except Exception as e:
            print(e)
            continue
        data = raw_data
        # data = [list(line) for line in raw_data]
        # print('评论个数: ', len(raw_data))
        fw = nrams.FreqPhrase(min_count=10, threshold=0.4)  # 不使用分隔符
        for item, value in fw.combine2words(data).items():
            result.append([attraction_name, len(data), ''.join(item), value[0]])

    print('run time 1:', time.time()-start)

    with open('../../data/data_output/乐山大佛_频繁子序列-1.txt', 'w') as f:
        csv.writer(f).writerows(result)


    """方法二：不分词，以单个字符为粒度检测频繁子序列，使用各种标点符号作为分隔符"""
    start = time.time()
    for i in range(1):
        # print(i)
        result = []
        ws = segmentation.WordSegmentation()
        try:
            raw_data = ws.read_data(file_path)
        except Exception as e:
            print(e)
            continue
        data = raw_data
        # data = [list(line) for line in raw_data]
        # print('评论个数: ', len(raw_data))
        fw = nrams.FreqPhrase(min_count=10, threshold=0.4, stopwords_file=stopwords_file)
        for item, value in fw.combine2words(data).items():
            result.append([attraction_name, len(data), ''.join(item), value[0]])

    print('run time 2:', time.time()-start)

    with open('../../data/data_output/乐山大佛_频繁子序列-2.txt', 'w') as f:
        csv.writer(f).writerows(result)

    """方法三：分词，以分词结果为粒度检测频繁子序列，不使用各种标点符号作为分隔符"""
    start = time.time()
    for i in range(1):
        # print(i)
        result = []
        ws = segmentation.WordSegmentation()
        try:
            data = ws.segmentation(file_path)
        except Exception as e:
            print(e)
            continue
        fw = nrams.FreqPhrase(min_count=10, threshold=0.4)
        for item, value in fw.combine2words(data).items():
            result.append([attraction_name, len(data), ''.join(item), value[0]])

    print('run time 3:', time.time()-start)

    with open('../../data/data_output/乐山大佛_频繁子序列-3.txt', 'w') as f:
        csv.writer(f).writerows(result)

    """方法四：分词，以分词结果为粒度检测频繁子序列，使用各种标点符号作为分隔符"""
    start = time.time()
    for i in range(1):
        # print(i)
        result = []
        ws = segmentation.WordSegmentation()
        try:
            data = ws.segmentation(file_path)
        except Exception as e:
            print(e)
            continue
        # print('评论个数: ', len(raw_data))
        fw = nrams.FreqPhrase(min_count=10, threshold=0.4, stopwords_file=stopwords_file)
        for item, value in fw.combine2words(data).items():
            result.append([attraction_name, len(data), ''.join(item), value[0]])

    print('run time 4:', time.time()-start)

    with open('../../data/data_output/乐山大佛_频繁子序列-4.txt', 'w') as f:
        csv.writer(f).writerows(result)


def reviews_frequent_subsequence(output_file):
    """使用方法四，遍历所有评论文件，写入一个txt"""
    start = time.time()
    for parent, dirnames, filenames in os.walk('/Users/monabai/Desktop/data/pinglun'):
        print(len(filenames))
        result = []
        for filename in filenames:
            attraction_name = filename[:-4]
            if attraction_name != 'pinglun':
                file_path = '/Users/monabai/Desktop/data/pinglun/' + attraction_name + '.txt'
                # print(file_path)
                ws = segmentation.WordSegmentation()
                try:
                    data = ws.segmentation(file_path)
                except Exception as e:
                    print(e)
                    continue
                fw = nrams.FreqPhrase(min_count=10, threshold=0.4, stopwords_file=stopwords_file)
                for item, value in fw.combine2words(data).items():
                    # 景点名，评论数量，频繁子序列，频繁子序列出现次数
                    result.append([attraction_name, len(data), ''.join(item), value[0]])
            with open(output_file, 'w') as f:
                csv.writer(f).writerows(result)

    print('run time:', time.time()-start)


if __name__ == '__main__':
    attraction_name = '乐山大佛'
    # attraction_name = '白云山'
    stopwords_file = '../../data/stopwords/stopwords_marks.txt'
    # test(attraction_name, stopwords_file)
    output_file = '../../data/data_output/reviews_频繁子序列-4.txt'
    # reviews_frequent_subsequence(output_file)

    import jieba
    start = time.time()
    data = []
    raw_data = ['<div class="review-nav">        <ul class="clearfix">            <li data-type="0" data-category="0" class="on"><span class="divide"></span><a href="javascript:void(0);"><span>全部</span></a></li>                                                    <li data-type="1" data-category="12" class="">                    <span class="divide"></span>                    <a href="javascript:void(0);">                        <span>中评</span>                        <span class="num">（1条）</span>                    </a>                </li>                                                        </ul>    </div>']
    for item in raw_data:
        data.append([x for x in jieba.cut(item)])  # 使用精确模式
    result = []
    fw = nrams.FreqPhrase(min_count=1, threshold=0, stopwords_file=stopwords_file)
    for item, value in fw.combine2words(data).items():
        # 景点名，评论数量，频繁子序列，频繁子序列出现次数
        result.append(['test', len(data), ''.join(item), value[0]])
    print('run time:', time.time() - start)
    print(result)
