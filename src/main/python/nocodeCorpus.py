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
    corpus = open('corpus/nocode%s.dat' % corpusName, "w")
    commitCorpus = open('corpus/commit%s.dat' % corpusName, "w")
    issueCorpus = open('corpus/issue%s.dat' % corpusName, "w")
    try:
        print 'start'
        try:
            # commit part
            gitRe = gitResolver.GitResolver(repoPath)
            commits = gitRe.getCommits()
            print repoPath, ":", len(commits)
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
            issues = mysqlOperator.selectAllIssueInOneRepo(repoId)
            print repoId, ":", len(issues)
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
            print "***", repoId, ":", e
            print traceback.format_exc()
        print 'end'
    except IOError, e:
        print "***", e
        print traceback.format_exc()
    finally:
        corpus.close()
        commitCorpus.close()
        issueCorpus.close()


def buildEmbedding(repo_id):
    sentences3 = word2vec.Text8Corpus("corpus/nocode%d.dat" % repo_id)
    model3 = word2vec.Word2Vec(sentences3, size=VECTOR_SIZE, sg=1, hs=1, iter=50)
    model3.save("test/nocode%d.model" % repo_id)


if __name__ == '__main__':
    index = nocodeRepoInfo.USE_REPO_INDEX
    buildIssueAndCommitSeq(nocodeRepoInfo.REPO_MAP[index]['id'], nocodeRepoInfo.REPO_MAP[index]['path'], str(nocodeRepoInfo.REPO_MAP[index]['id']))
    buildEmbedding(nocodeRepoInfo.REPO_MAP[index]['id'])
