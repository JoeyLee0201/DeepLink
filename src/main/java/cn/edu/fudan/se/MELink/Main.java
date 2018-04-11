package cn.edu.fudan.se.MELink;

import java.io.IOException;

import cn.edu.fudan.se.MELink.nlp.FileOperator;
import cn.edu.fudan.se.MELink.nlp.StandfordParser;
import cn.edu.fudan.se.MELink.util.StringUtils;
import cn.edu.fudan.se.MELink.webuild.CorpusBuilder;

public class Main {

    public static void main(String[] args){
//    	try {
//			new CorpusBuilder("model.dat").build();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
//    	System.out.println(new StandfordParser().parse("2.x: marble additions and updates (12/11) (#5759)"));
    	try {
			new FileOperator("corpus/model.dat","corpus/words.dat").deal();
		} catch (IOException e) {
			e.printStackTrace();
		}
    }
}
