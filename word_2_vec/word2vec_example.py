#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: pacman
@time: 2017/10/23 14:37
"""
import gensim
# from gensim.models.word2vec import  Word2Vec


def most_similar(word, num=50):
    model_path = 'C:\\data\\zh_wiki_vectors.bin'
    # model = gensim.models.Word2Vec.load_word2vec_format(model_path, binary=True)
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    # model = Word2Vec.load_word2vec_format(model_path, binary=True)
    return model.most_similar(word, topn=num)
    # print(model["good"])

def run(word):
    results = most_similar(word)
    for item in results:
        print('{}\t{:0.4f}\n'.format(item[0], item[1]), end='')


def main():
    word = '礼貌'
    run(word)


if __name__ == '__main__':
    main()
