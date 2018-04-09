package cn.edu.fudan.se.MELink.mybatis.mapper;

import java.util.List;

import cn.edu.fudan.se.MELink.mybatis.bean.ProjectInfo;

public interface ProjectInfoMapper {
	public void insertProjectInfo(ProjectInfo info);
	public void updateProjectInfo(ProjectInfo info);
	public void updateProjectInfoByMoreFive(ProjectInfo info);
	List<ProjectInfo> selectAllInfo();
	
	List<ProjectInfo> selectCodeOver(int codeLoc);
}
