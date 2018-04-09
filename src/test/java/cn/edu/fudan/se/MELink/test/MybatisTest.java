package cn.edu.fudan.se.MELink.test;

import org.junit.Test;

import cn.edu.fudan.se.MELink.mybatis.dao.ProjectInfoDao;

public class MybatisTest {
	@Test
	public void projectTest(){
		System.out.println(ProjectInfoDao.getInstance().selectAllInfo().size());
	}
}
