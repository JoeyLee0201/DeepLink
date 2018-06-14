# -*- coding: UTF-8 -*-

from database import mysqlOperator
from database import linkOperator
from gitresolver import gitResolver
from preprocessor import preprocessor
import re
import traceback
import sys

reload(sys)

sys.setdefaultencoding('utf-8')


def getPath(s):
    temp = re.sub(r'https://github.com/', '', s, 0, re.I)
    return "/home/fdse/data/prior_repository/"+temp


def buildIssueAndCommit():
    repos = linkOperator.selectOneRepo(50904245)
    # repos = linkOperator.selectRepoOver(5000)
    corpus = open('nocode50904245.dat', "w")
    commitCorpus = open('commit50904245.dat', "w")
    issueCorpus = open('issue50904245.dat', "w")
    try:
        print 'start'
        for highRepo in repos:
            try:
                # commit part
                path = getPath(highRepo[1])
                gitRe = gitResolver.GitResolver(path)
                commits = gitRe.getCommits()
                print path, ":", len(commits)
                for commit in commits:
                    words = preprocessor.preprocessToWord(commit.message.decode('utf-8'))
                    if len(words):
                        # 不是空列表
                        for word in words:
                            corpus.write(word.encode('utf-8'))
                            corpus.write(" ")
                            commitCorpus.write(word.encode('utf-8'))
                            commitCorpus.write(" ")
                        corpus.write("\n")
                        commitCorpus.write("\n")
                # issue part
                issues = mysqlOperator.selectAllIssueInOneRepo(highRepo[0])
                print highRepo[0], ":", len(issues)
                for issue in issues:
                    titleWords = preprocessor.preprocessToWord(issue[4].decode('utf-8'))
                    if len(titleWords):
                        # 不是空列表
                        for word in titleWords:
                            corpus.write(word.encode('utf-8'))
                            corpus.write(" ")
                            issueCorpus.write(word.encode('utf-8'))
                            issueCorpus.write(" ")
                        corpus.write("\n")
                        issueCorpus.write("\n")
                    if issue[5]:
                        body = preprocessor.processHTML(issue[5].decode('utf-8'))
                        bodyWords = body[1]
                        if len(bodyWords):
                            # 不是空列表
                            for word in bodyWords:
                                corpus.write(word.encode('utf-8'))
                                corpus.write(" ")
                                issueCorpus.write(word.encode('utf-8'))
                                issueCorpus.write(" ")
                            corpus.write("\n")
                            issueCorpus.write("\n")
            except BaseException, e:
                print "***", highRepo[0], ":", e
                print traceback.format_exc()
        print 'end'
    except IOError, e:
        # 检查open()是否失败，通常是IOError类型的错误
        print "***", e
        print traceback.format_exc()
    finally:
        corpus.close()
        commitCorpus.close()
        issueCorpus.close()


def buildIssueAndCommitSeq():
    corpus = open('corpus/nocode50904245-1.dat', "w")
    commitCorpus = open('corpus/commit50904245-1.dat', "w")
    issueCorpus = open('corpus/issue50904245-1.dat', "w")
    try:
        print 'start'
        try:
            # commit part
            gitRe = gitResolver.GitResolver('/home/fdse/user/rh/gitrepo/apache/beam')
            commits = gitRe.getCommits()
            print '/home/fdse/user/rh/gitrepo/apache/beam', ":", len(commits)
            for commit in commits:
                seqs = preprocessor.preprocessNoCamel(commit.message.decode('utf-8'))
                if len(seqs):
                    # 不是空列表
                    for seq in seqs:
                        for word in seq:
                            corpus.write(word.encode('utf-8'))
                            corpus.write(" ")
                            commitCorpus.write(word.encode('utf-8'))
                            commitCorpus.write(" ")
                        corpus.write("\n")
                        commitCorpus.write("\n")
            # issue part
            issues = mysqlOperator.selectAllIssueInOneRepo(50904245)
            print "50904245 :", len(issues)
            for issue in issues:
                titleSeqs = preprocessor.preprocessNoCamel(issue[4].decode('utf-8'))
                if len(titleSeqs):
                    # 不是空列表
                    for titleSeq in titleSeqs:
                        for word in titleSeq:
                            corpus.write(word.encode('utf-8'))
                            corpus.write(" ")
                            issueCorpus.write(word.encode('utf-8'))
                            issueCorpus.write(" ")
                        corpus.write("\n")
                        issueCorpus.write("\n")
                if issue[5]:
                    body = preprocessor.processHTMLNoCamel(issue[5].decode('utf-8'))
                    if len(body):
                        # 不是空列表
                        for bodySeq in body:
                            for word in bodySeq:
                                corpus.write(word.encode('utf-8'))
                                corpus.write(" ")
                                issueCorpus.write(word.encode('utf-8'))
                                issueCorpus.write(" ")
                            corpus.write("\n")
                            issueCorpus.write("\n")
        except BaseException, e:
            print "*** 50904245 :", e
            print traceback.format_exc()
        print 'end'
    except IOError, e:
        print "***", e
        print traceback.format_exc()
    finally:
        corpus.close()
        commitCorpus.close()
        issueCorpus.close()


if __name__ == '__main__':
    buildIssueAndCommitSeq()
