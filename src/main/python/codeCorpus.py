# -*- coding: UTF-8 -*-

from database import mysqlOperator
from gitresolver import gitResolver
from preprocessor import preprocessor
from gensim.models import word2vec

import logging
import traceback
import sys
import nocodeRepoInfo

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

VECTOR_SIZE = nocodeRepoInfo.VECTOR_SIZE


def buildIssueAndCommitSeq(repoId, repoPath, corpusName):
    corpus = open('corpus/code%s.dat' % corpusName, "w")
    try:
        print 'start'
        try:
            # commit part
            gitRe = gitResolver.GitResolver(repoPath)
            commits = gitRe.getCommits()
            print repoPath, ":", len(commits)
            for commit in commits:
                diffs = gitRe.getOneDiff(commit)
                for diff in diffs:
                    diffCode = preprocessor.processDiffCode(diff.diff)
                    if len(diffCode):
                        for word in diffCode:
                            corpus.write(word.encode('utf-8'))
                            corpus.write(" ")
                        corpus.write("\n")

            # issue part
            issues = mysqlOperator.selectAllIssueInOneRepo(repoId)
            print repoId, ":", len(issues)
            for issue in issues:
                if issue[5]:
                    bodycode = preprocessor.getIssueCode(issue[5].decode('utf-8'))
                    if len(bodycode):
                        # 不是空列表
                        for word in bodycode:
                            corpus.write(word.encode('utf-8'))
                            corpus.write(" ")
                        corpus.write("\n")
        except BaseException, e:
            print "***", repoId, ":", e
            print traceback.format_exc()
        print 'end'
    except IOError, e:
        print "***", e
        print traceback.format_exc()
    finally:
        corpus.close()


def buildEmbedding(repo_id):
    sentences3 = word2vec.Text8Corpus("corpus/code%d.dat" % repo_id)
    model3 = word2vec.Word2Vec(sentences3, size=VECTOR_SIZE, sg=1, hs=1, iter=50)
    model3.save("test/code%d.model" % repo_id)


if __name__ == '__main__':
    index = nocodeRepoInfo.USE_REPO_INDEX
    buildIssueAndCommitSeq(nocodeRepoInfo.REPO_MAP[index]['id'], nocodeRepoInfo.REPO_MAP[index]['path'], str(nocodeRepoInfo.REPO_MAP[index]['id']))
    buildEmbedding(nocodeRepoInfo.REPO_MAP[index]['id'])
