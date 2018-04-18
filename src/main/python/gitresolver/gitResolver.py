# -*- coding: UTF-8 -*-

import git
import time

class GitResolver:
    def __init__(self, gitPath):
        self.gitPath = gitPath
        self.repo = git.Repo(gitPath)

    def getCommits(self):
        return list(self.repo.iter_commits())

    def getDiff(self, a_commit, b_commit):
        return self.repo.diff(a_commit, b_commit)

    def close(self):
        self.repo.close()

    def getDiffs(self):
        diffs = []
        commits = self.getCommits()
        for commit in commits:
            if len(commit.parents) == 1:#删除merge节点
                parent = commit.parents[0]
                diffs.append(commit.diff(parent))
        return diffs

    def getOneDiff(self, commit):
        if len(commit.parents) != 1 :
            return None
        # print self.repo.git.show(commit)
        diffs = list(commit.parents[0].diff(commit, create_patch=True, ignore_blank_lines=True, ignore_space_at_eol=True, diff_filter='cr').iter_change_type('M'))
        result = []
        for diff in diffs:
            if diff.a_path.endswith('.java'):
                result.append(diff)
        return result

    def getCommitDate(self, commit):
        commitdDate = time.gmtime(commit.committed_date)
        return str(commitdDate.tm_year)+"-"+str(commitdDate.tm_mon)+"-"+str(commitdDate.tm_mday)