# -*- coding: UTF-8 -*-

from database import mysqlOperator
from gitresolver import gitResolver
from preprocessor import preprocessor
import re

import sys

reload(sys)

sys.setdefaultencoding('utf-8')

def buildFromGit():
    repos = mysqlOperator.selectAllHighRepository()
    corpus = open('corpusLabel.dat', "w") 
    try:
        for highRepo in repos:
            path = getPath(highRepo[1])
            try:
                gitRe = gitResolver.GitResolver(path)
                commits = gitRe.getCommits()
                print path,":",len(commits)
                for commit in commits:
                    corpus.write(str(highRepo[0]).encode("utf-8"))
                    corpus.write("\n")
                    corpus.write(commit.hexsha.encode("utf-8"))
                    corpus.write("\n")
                    sens=preprocessor.preprocess(commit.message.decode('utf-8'))
                    for sentence in sens:
                        if len(sentence):#不是空列表
                            for word in sentence:
                                corpus.write(word.encode('utf-8'))
                                corpus.write(" ")
                            corpus.write("\n")
                    corpus.write("\n")
            except BaseException,e:
                print "***",path,":",e
    except IOError,e:#检查open()是否失败，通常是IOError类型的错误
        print "***",e
    finally:
        corpus.close()

def getPath(s):
    temp = re.sub(r'https://github.com/', '', s, 0, re.I)
    return "/home/fdse/Downloads/high/high_quality_repos/"+temp;

def buildModelFromFile(filename):
    with open(filename, "rb") as corpus:
        repoId = corpus.readline()
        while repoId:
            repoId = repoId.strip().strip('\n')
            commitId = corpus.readline().strip().strip('\n')
            line = corpus.readline().strip('\n')
            content = ''
            while line:
                if not len(line.strip()):
                    break
                content = content +' '+line
                line = corpus.readline().strip('\n')
            print "sum:",repoId,commitId,content
            word_list = content.strip().split(' ')
            print word_list
            repoId = corpus.readline()
    print "end"

if __name__ == '__main__':
    print buildModelFromFile('corpusLabel.dat')