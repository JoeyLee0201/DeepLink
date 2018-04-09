package cn.edu.fudan.se.MELink.test;

import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;

import org.junit.Test;

public class FileTest {
	@Test
	public void fileTest() throws IOException{
		try(BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("test.dat", true))){
			for(int i = 0; i < 100; i++){
					bos.write("I am testing the file test case. It is so boring.".getBytes());
					bos.write("\n".getBytes());
			}
		}
	}
}
