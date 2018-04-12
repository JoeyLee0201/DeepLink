package cn.edu.fudan.se.MELink.webuild;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.List;

import org.eclipse.jgit.revwalk.RevCommit;

import cn.edu.fudan.se.MELink.git.GitReader;
import cn.edu.fudan.se.MELink.mybatis.bean.ProjectInfo;
import cn.edu.fudan.se.MELink.mybatis.dao.ProjectInfoDao;
import cn.edu.fudan.se.MELink.nlp.StandfordParser;
import cn.edu.fudan.se.MELink.util.PathUtils;

public class CorpusBuilder {
	private String fileName;
	
	public CorpusBuilder(String fileName){
		this.fileName = fileName;
	}
	
	public void build() throws IOException{
		List<ProjectInfo> projects = ProjectInfoDao.getInstance().selectAllInfo();
		try(BufferedWriter bos = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileName, true),"utf-8"))){
			for(ProjectInfo p : projects){
				GitReader gitReader = new GitReader(PathUtils.changeHighWebsite2Path(p.getWebsite()));
				try {
					gitReader.init();
				} catch (IOException e) {
					System.out.println(p.getWebsite());
					gitReader=null;
				}
				if(gitReader==null) continue;
				
				List<RevCommit> commits = gitReader.getCommits();
				for(RevCommit commit: commits){
					bos.write(commit.getFullMessage());
					bos.write("\n");
				}
			}
		}
	}
	
	public void directBuild() throws IOException{
		List<ProjectInfo> projects = ProjectInfoDao.getInstance().selectAllInfo();
		try(BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileName, true),"utf-8"))){
			for(ProjectInfo p : projects){
				GitReader gitReader = new GitReader(PathUtils.changeHighWebsite2Path(p.getWebsite()));
				try {
					gitReader.init();
				} catch (IOException e) {
					System.out.println(p.getWebsite());
					gitReader=null;
				}
				if(gitReader==null) continue;
				
				List<RevCommit> commits = gitReader.getCommits();
				for(RevCommit commit: commits){
					StandfordParser.parseCommit(commit, bw);
				}
			}
		}
	}
}
