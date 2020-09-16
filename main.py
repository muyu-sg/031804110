# -*- coding: utf-8 -*-
import sys
import jieba
import jieba.analyse
import os
import numpy as np
from MyException import emptyText_error,noChinese_error
def get_keywords(context1,context2):
    # 去除停用词
    stopwords = [line.strip() for line in open('stopWords.txt',encoding='UTF-8').readlines()]
    stopwords.append("\n")
    # 分词
    keywords1 =[i for i in jieba.cut(context1, cut_all=True) if i != '' and i!=' ']
    keywords2 = [i for i in jieba.cut(context2, cut_all=True) if i != '' and i!=' ']
    # 对两个关键词列表进行合并去重
    union = set(keywords1).union(set(keywords2)) - set(stopwords)
    return keywords1,keywords2,union
def get_freq(keywords1,keywords2,union):
    #获取词频向量
    dist_freq1 = {}
    dist_freq2 = {}
    for x in union:
        dist_freq1[x] = keywords1.count(x)
        dist_freq2[x] = keywords2.count(x)
    # # 遍历分词后的结果集，计算每个词出现的频率
    freq1 = [keywords1.count(x) for x in union]
    freq2 = [keywords2.count(x) for x in union]
    return freq1,freq2
def CosineSimilarity(freq1, freq2):
    # 余弦相似度计算
    sim= float(np.dot(freq1,freq2) / (np.linalg.norm(freq1) * np.linalg.norm(freq2)))
    return sim
def check_contain_chinese(check_str):
    # 中文字符的编码范围是：
    # \u4e00 - \u9fff
    # 只要编码在此范围就可判断为中文字符
    for ch in check_str.decode('utf-8'):
         if u'\u4e00' <= ch <= u'\u9fff':
             return False
    return True
def main():
    #输入文件绝对路径，arg1，arg2为要查重的文件，arg3为答案文件
    arg1, arg2, arg3 = sys.argv[1], sys.argv[2], sys.argv[3]
    text1 = open(arg1, 'rb')
    text2 = open(arg2, 'rb')
    orig = text1.read()  # 读取文件
    orig_add = text2.read()
    # 空文本异常
    if(len(orig)==0 or len(orig_add)==0):
        text1.close()
        text2.close()
        raise emptyText_error
    if(check_contain_chinese(orig_add)):
        raise noChinese_error
    ans = open(arg3, 'w+')  # 如果输出文件不存在则创建，存在则覆盖
    # 获取关键词
    keywords1,keywords2,union=get_keywords(orig,orig_add)
    # 获取词频向量
    freq1,freq2=get_freq(keywords1,keywords2,union)
    # 计算余弦值
    similarity = CosineSimilarity(freq1,freq2)
    # 获取文件名
    orig_filename = arg1[len(os.path.dirname(arg1)) + 1:]
    orig_add_filename = arg2[len(os.path.dirname(arg2)) + 1:]
    sim = "{}和{}的重复率为{:.2f}".format(orig_filename, orig_add_filename, similarity)
    print(sim)
    ans.write(sim)
    text1.close()
    text2.close()
    ans.close()
    return 0


if __name__ == '__main__':
  main()