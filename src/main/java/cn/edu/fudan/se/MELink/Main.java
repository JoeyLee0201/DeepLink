package cn.edu.fudan.se.MELink;

import java.io.IOException;

import cn.edu.fudan.se.MELink.webuild.CorpusBuilder;

public class Main {

    public static void main(String[] args){
    	try {
			new CorpusBuilder("model.dat").build();
		} catch (IOException e) {
			e.printStackTrace();
		}
    }
}
