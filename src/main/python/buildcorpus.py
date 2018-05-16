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


def buildCommitPart():
    repos = linkOperator.selectRepoOver(5000)
    logCorpus = open('commitLog.dat', "w")
    codeCorpus = open('commitCode.dat', "w")
    try:
        print 'start'
        for highRepo in repos:
            path = getPath(highRepo[1])
            try:
                gitRe = gitResolver.GitResolver(path)
                commits = gitRe.getCommits()
                print path, ":", len(commits)
                for commit in commits:
                    words = preprocessor.preprocessToWord(commit.message.decode('utf-8'))
                    if len(words):
                        # 不是空列表
                        for word in words:
                            logCorpus.write(word.encode('utf-8'))
                            logCorpus.write(" ")
                        logCorpus.write("\n")
                    diffs = gitRe.getOneDiff(commit)
                    for diff in diffs:
                        diffCode = preprocessor.processDiffCode(diff.diff)
                        if len(diffCode):
                            for code in diffCode:
                                codeCorpus.write(code)
                                codeCorpus.write(" ")
                            codeCorpus.write("\n")
            except BaseException, e:
                print "***", path, ":", e
                print traceback.format_exc()
        print 'end'
    except IOError,e:
        # 检查open()是否失败，通常是IOError类型的错误
        print "***",e
        print traceback.format_exc()
    finally:
        logCorpus.close()
        codeCorpus.close()


def buildIssuePart():
    repos = linkOperator.selectRepoOver(5000)
    textCorpus = open('issueText.dat', "w")
    codeCorpus = open('issueCode.dat', "w")
    try:
        print 'start'
        for highRepo in repos:
            try:
                issues = mysqlOperator.selectAllIssueInOneRepo(highRepo[0])
                print highRepo[0], ":", len(issues)
                for issue in issues:
                    titleWords = preprocessor.preprocessToWord(issue[4].decode('utf-8'))
                    if len(titleWords):
                        # 不是空列表
                        for word in titleWords:
                            textCorpus.write(word.encode('utf-8'))
                            textCorpus.write(" ")
                        textCorpus.write("\n")
                    if issue[5]:
                        body = preprocessor.processHTML(issue[5].decode('utf-8'))
                        bodyWords = body[1]
                        codeWords = body[0]
                        if len(bodyWords):
                            # 不是空列表
                            for word in bodyWords:
                                textCorpus.write(word.encode('utf-8'))
                                textCorpus.write(" ")
                            textCorpus.write("\n")
                        if len(codeWords):
                            # 不是空列表
                            for word in codeWords:
                                codeCorpus.write(word.encode('utf-8'))
                                codeCorpus.write(" ")
                            codeCorpus.write("\n")
                    comments = mysqlOperator.selectCommentInOneIssue(issue[1])
                    for comment in comments:
                        temp = preprocessor.processHTML(comment[4].decode('utf-8'))
                        cBodyWords = temp[1]
                        cCodeWords = temp[0]
                        if len(cBodyWords):
                            # 不是空列表
                            for word in cBodyWords:
                                textCorpus.write(word.encode('utf-8'))
                                textCorpus.write(" ")
                            textCorpus.write("\n")
                        if len(cCodeWords):
                            # 不是空列表
                            for word in cCodeWords:
                                codeCorpus.write(word.encode('utf-8'))
                                codeCorpus.write(" ")
                            codeCorpus.write("\n")
            except BaseException, e:
                print "***", highRepo[0], ":", e
                print traceback.format_exc()
        print 'end'
    except IOError, e:
        # 检查open()是否失败，通常是IOError类型的错误
        print "***", e
        print traceback.format_exc()
    finally:
        textCorpus.close()
        codeCorpus.close()


def getPath(s):
    temp = re.sub(r'https://github.com/', '', s, 0, re.I)
    return "/home/fdse/data/prior_repository/"+temp;


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
            print "sum:", repoId, commitId, content
            word_list = content.strip().split(' ')
            print word_list
            repoId = corpus.readline()
    print "end"


def buildIssueAndCommit():
    repos = linkOperator.selectOneRepo(12983151)
    # repos = linkOperator.selectRepoOver(5000)
    textCorpus = open('text.dat', "w")
    codeCorpus = open('code.dat', "w")
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
                            textCorpus.write(word.encode('utf-8'))
                            textCorpus.write(" ")
                        textCorpus.write("\n")
                    diffs = gitRe.getOneDiff(commit)
                    for diff in diffs:
                        diffCode = preprocessor.processDiffCode(diff.diff)
                        preDiffCode = preprocessor.processPreDiffCode(diff.diff)
                        if len(diffCode):
                            for code in diffCode:
                                codeCorpus.write(code)
                                codeCorpus.write(" ")
                            codeCorpus.write("\n")
                        if len(preDiffCode):
                            for code in preDiffCode:
                                codeCorpus.write(code)
                                codeCorpus.write(" ")
                            codeCorpus.write("\n")
                # issue part
                issues = mysqlOperator.selectAllIssueInOneRepo(highRepo[0])
                print highRepo[0], ":", len(issues)
                for issue in issues:
                    titleWords = preprocessor.preprocessToWord(issue[4].decode('utf-8'))
                    if len(titleWords):
                        # 不是空列表
                        for word in titleWords:
                            textCorpus.write(word.encode('utf-8'))
                            textCorpus.write(" ")
                        textCorpus.write("\n")
                    if issue[5]:
                        body = preprocessor.processHTML(issue[5].decode('utf-8'))
                        bodyWords = body[1]
                        codeWords = body[0]
                        if len(bodyWords):
                            # 不是空列表
                            for word in bodyWords:
                                textCorpus.write(word.encode('utf-8'))
                                textCorpus.write(" ")
                            textCorpus.write("\n")
                        if len(codeWords):
                            # 不是空列表
                            for word in codeWords:
                                codeCorpus.write(word.encode('utf-8'))
                                codeCorpus.write(" ")
                            codeCorpus.write("\n")
                    comments = mysqlOperator.selectCommentInOneIssue(issue[1])
                    for comment in comments:
                        temp = preprocessor.processHTML(comment[4].decode('utf-8'))
                        cBodyWords = temp[1]
                        cCodeWords = temp[0]
                        if len(cBodyWords):
                            # 不是空列表
                            for word in cBodyWords:
                                textCorpus.write(word.encode('utf-8'))
                                textCorpus.write(" ")
                            textCorpus.write("\n")
                        if len(cCodeWords):
                            # 不是空列表
                            for word in cCodeWords:
                                codeCorpus.write(word.encode('utf-8'))
                                codeCorpus.write(" ")
                            codeCorpus.write("\n")
            except BaseException, e:
                print "***", highRepo[0], ":", e
                print traceback.format_exc()
        print 'end'
    except IOError, e:
        # 检查open()是否失败，通常是IOError类型的错误
        print "***", e
        print traceback.format_exc()
    finally:
        textCorpus.close()
        codeCorpus.close()


if __name__ == '__main__':
    if sys.argv[1] == '1':
        buildCommitPart()
    elif sys.argv[1] == '2':
        buildIssuePart()
    elif sys.argv[1] == '3':
        buildIssueAndCommit()
    else:
        print 'please select 1(commit) or 2(issue) or 3(both)'
