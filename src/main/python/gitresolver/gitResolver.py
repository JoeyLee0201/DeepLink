# -*- coding: UTF-8 -*-

import git
import time
import datetime

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
            if len(commit.parents) == 1:
                # 删除merge节点
                parent = commit.parents[0]
                diffs.append(commit.diff(parent))
        return diffs

    def getOneDiff(self, commit):
        if len(commit.parents) != 1:
            return []
        # print self.repo.git.show(commit)
        diffs = list(commit.parents[0].diff(commit, create_patch=True, ignore_blank_lines=True,
                                            ignore_space_at_eol=True, diff_filter='cr', unified=0).iter_change_type('M'))
        result = []
        for diff in diffs:
            if diff.a_path.endswith('.java'):
                result.append(diff)
        return result

    def getDateTime(self, commit):
        return datetime.datetime.fromtimestamp(commit.committed_date)

    def getOneCommit(self, sha):
        return self.repo.commit(sha)

    def getFiles(self, sha):
        result = []
        commit = self.repo.commit(sha)
        if len(commit.parents) == 1:
            # changed_files = [item.a_path for item in commit.diff(commit.parents[0])]
            changed_files = commit.parents[0].diff(commit)
            for changeFile in changed_files:
                # print changeFile.a_path, ":", changeFile.change_type
                if changeFile.change_type == 'A' or changeFile.change_type == 'M':
                    result.append({'path': changeFile.a_path, 'text': commit.tree[changeFile.a_path].data_stream.read()})
        return result

