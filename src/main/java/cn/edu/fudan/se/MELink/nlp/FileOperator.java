package cn.edu.fudan.se.MELink.nlp;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

import cn.edu.fudan.se.MELink.util.StringUtils;

public class FileOperator {
	private String toDealFile;
	private String newFile;
	private StandfordParser parser;
	public FileOperator(String toDealFile, String newFile){
		this.toDealFile = toDealFile;
		this.newFile = newFile;
		parser = new StandfordParser();
	}
	public void deal() throws IOException{
		// clear toDealFile 
		try(BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(newFile),"utf-8"));
				BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(toDealFile),"utf-8"))){
			br.lines().forEach(s->{
				try {
					if(s!=null && s.length()!=0){
//						System.out.println("\n".equals(s)+"\t"+s.length()+":"+s);
						bw.write(StringUtils.link(parser.parse(s)));
					}else{
						bw.write("\n");
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			});
		}
	}
}
