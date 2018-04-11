package cn.edu.fudan.se.MELink.nlp;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class FileOperator {
	private String toDealFile;
	private String newFile;
	public FileOperator(String toDealFile, String newFile){
		this.toDealFile = toDealFile;
		this.newFile = newFile;
	}
	public void deal() throws IOException{
		try(BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(newFile, true),"utf-8"));
				BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(toDealFile),"utf-8"))){
			
		}
	}
}
