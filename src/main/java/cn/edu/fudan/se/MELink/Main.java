package cn.edu.fudan.se.MELink;

import java.io.IOException;

import cn.edu.fudan.se.MELink.nlp.StandfordParser;
import cn.edu.fudan.se.MELink.webuild.CorpusBuilder;

public class Main {

    public static void main(String[] args){
    	try {
			new CorpusBuilder("model.dat").build();
		} catch (IOException e) {
			e.printStackTrace();
		}
    	new StandfordParser().parse("I have bootstrapped this doc with things that should not be controversial, just statements of fact of what exists. If any are controversial, I apologize, please open a PR with the recommended change.");
    }
}
