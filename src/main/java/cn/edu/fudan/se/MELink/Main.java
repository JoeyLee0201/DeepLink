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
    	System.out.println(StandfordParser.parse("Removed use of deprecated API from tests & operators, fixed year in head..."));
//    	try {
//			new FileOperator("corpus/model.dat","corpus/words2.dat").deal();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
//    	System.out.println("============================================over===================================================");
    }
}
