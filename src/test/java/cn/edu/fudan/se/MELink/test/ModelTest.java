package cn.edu.fudan.se.MELink.test;

import java.io.IOException;

import org.junit.Test;

import cn.edu.fudan.se.MELink.webuild.ModelHandler;

public class ModelTest {
	@Test
	public void loadTest(){
		ModelHandler handler = new ModelHandler("D:/javaee/parser/MELink/src/main/python/words2.model");
		try {
			handler.init();
		} catch (IOException e) {
			e.printStackTrace();
		}
		handler.getSamWord("fix", 20);
	}
}
