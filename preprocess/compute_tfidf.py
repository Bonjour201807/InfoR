"""
@Author  : monabai
@Time    : 2018/7/25 11:01
@Software: PyCharm
@File    : compute_tfidf.py
"""
import jieba
import jieba.posseg as pseg
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora, models, similarities
import numpy as np
from tqdm import tqdm

raw_documents = [
    '0无偿居间介绍买卖毒品的行为应如何定性',
    '1吸毒男动态持有大量毒品的行为该如何认定',
    '2如何区分是非法种植毒品原植物罪还是非法制造毒品罪'
    # '3为毒贩贩卖毒品提供帮助构成贩卖毒品罪',
    # '4将自己吸食的毒品原价转让给朋友吸食的行为该如何认定',
    # '5为获报酬帮人购买毒品的行为该如何认定',
    # '6毒贩出狱后再次够买毒品途中被抓的行为认定',
    # '7虚夸毒品功效劝人吸食毒品的行为该如何认定',
    # '8妻子下落不明丈夫又与他人登记结婚是否为无效婚姻',
    # '9一方未签字办理的结婚登记是否有效',
    # '10夫妻双方1990年按农村习俗举办婚礼没有结婚证 一方可否起诉离婚',
    # '11结婚前对方父母出资购买的住房写我们二人的名字有效吗',
    # '12身份证被别人冒用无法登记结婚怎么办？',
    # '13同居后又与他人登记结婚是否构成重婚罪',
    # '14未办登记只举办结婚仪式可起诉离婚吗',
    # '15同居多年未办理结婚登记，是否可以向法院起诉要求离婚'
]

texts = [[word for word in jieba.cut(document, cut_all=True)] for document in raw_documents]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
count = 0
for item in corpus_tfidf:
    print(raw_documents[count])
    print(texts[count])
    print(item)
    count += 1

print(tfidf[corpus[-1]])
print('texts', texts)
print('corpous', corpus)
print('corpus_tfidf', corpus_tfidf)

def bow2vec(corpus_tfidf, dictionary):
    vec = []
    length = max(dictionary) + 1
    print('length', max(dictionary))
    for content in tqdm(corpus_tfidf):
        sentense_vectors = np.zeros(length)
        for co in content:
            sentense_vectors[co[0]] = co[1]
        vec.append(sentense_vectors)
    return vec

svec = bow2vec(corpus_tfidf, dictionary)
# print('svec', svec)


if __name__ == "__main__":
    corpus = ["我 来到 北京 清华大学",  # 第一类文本切词后的结果，词之间以空格隔开
              "他 来到 了 网易 杭研 大厦",  # 第二类文本的切词结果
              "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
              "我 爱 北京 天安门"]  # 第四类文本的切词结果
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print("-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print(word[j], weight[i][j])

    from gensim import corpora
    from collections import defaultdict
    from pprint import pprint
    documents = ["Human machine interface for lab abc computer applications",
                 "A survey of user opinion of computer system response time",
                 "The EPS user interface management system",
                 "System and human system engineering testing of EPS",
                 "Relation of user perceived response time to error measurement",
                 "The generation of random binary unordered trees",
                 "The intersection graph of paths in trees",
                 "Graph minors IV Widths of trees and well quasi ordering",
                 "Graph minors A survey"]
    stop_list = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stop_list]
             for document in documents]
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    print(frequency)
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    print('texts_2')
    pprint(texts)

