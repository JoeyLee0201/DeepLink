package cn.edu.fudan.se.MELink.git;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.api.errors.NoHeadException;
import org.eclipse.jgit.errors.AmbiguousObjectException;
import org.eclipse.jgit.errors.CorruptObjectException;
import org.eclipse.jgit.errors.IncorrectObjectTypeException;
import org.eclipse.jgit.errors.MissingObjectException;
import org.eclipse.jgit.errors.RevisionSyntaxException;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.ObjectLoader;
import org.eclipse.jgit.lib.ObjectReader;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.revwalk.RevTree;
import org.eclipse.jgit.revwalk.RevWalk;
import org.eclipse.jgit.treewalk.AbstractTreeIterator;
import org.eclipse.jgit.treewalk.CanonicalTreeParser;
import org.eclipse.jgit.treewalk.TreeWalk;

public class GitReader {
	private Git git;
	private Repository repository;
	private RevWalk revWalk;
	private String repositoryPath;
	
	public enum ChangeType {
		ADD,
		DELETE,
		CONTENT
	}
	
	public GitReader(String repositoryPath) {
		this.repositoryPath = repositoryPath;
	}
	
	public void init() throws IOException{
		git = Git.open(new File(repositoryPath));
		repository = git.getRepository();
		revWalk = new RevWalk(repository);
	}
	
	public List<RevCommit> getCommits(){
		List<RevCommit> allCommits = null;
		try {
			Iterable<RevCommit> commits = git.log().call();
			allCommits = new ArrayList<RevCommit>();
			for(RevCommit commit : commits){
				allCommits.add(commit);
			}
		} catch (NoHeadException e) {
			e.printStackTrace();
		} catch (GitAPIException e) {
			e.printStackTrace();
		} catch (NullPointerException e){
			e.printStackTrace();
		}
		return allCommits;
	}
	
	public RevCommit getOneCommit(String sha){
		ObjectId objId;
		try {
			objId = repository.resolve(sha);
			if (objId == null) {
				System.err.println("The commit: " + sha + " does not exist.");
				return null;
			}
			return revWalk.parseCommit(objId);
		} catch (RevisionSyntaxException e) {
			e.printStackTrace();
		} catch (AmbiguousObjectException e) {
			e.printStackTrace();
		} catch (IncorrectObjectTypeException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public AbstractTreeIterator prepareTreeParser(RevCommit commit){
    	try (RevWalk walk = new RevWalk(repository)) {
    		RevCommit temp = walk.parseCommit( commit.getId() );
            RevTree tree = walk.parseTree(temp.getTree().getId());

            CanonicalTreeParser oldTreeParser = new CanonicalTreeParser();
            try (ObjectReader oldReader = repository.newObjectReader()) {
                oldTreeParser.reset(oldReader, tree.getId());
            }
            walk.dispose();
            return oldTreeParser;
	    }catch (Exception e) {
			e.printStackTrace();
		}
    	return null;
    }
	
	public void walkCommit(RevCommit commit){
		System.out.println("\ncommit: " + commit.getName());
	    try (TreeWalk treeWalk = new TreeWalk(repository)) {
	        treeWalk.addTree(commit.getTree());
	        treeWalk.setRecursive(true);
	        while (treeWalk.next()) {
	            System.out.println("filename: " + treeWalk.getPathString());
	            ObjectId objectId = treeWalk.getObjectId(0);
	            ObjectLoader loader = repository.open(objectId);
	            loader.copyTo(System.out);
	        }
	    } catch (MissingObjectException e) {
			e.printStackTrace();
		} catch (IncorrectObjectTypeException e) {
			e.printStackTrace();
		} catch (CorruptObjectException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}    
	}
	
	public RevCommit getLastCommit(){
		RevCommit lastCommit = null;
		try {
			Iterable<RevCommit> commits = git.log().setMaxCount(1).call();
			for(RevCommit commit:commits){
				lastCommit = commit;
			}
		} catch (NoHeadException e) {
			e.printStackTrace();
		} catch (GitAPIException e) {
			e.printStackTrace();
		}
		return lastCommit;
	}
}
