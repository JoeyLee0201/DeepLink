package cn.edu.fudan.se.MELink.webuild;

import java.io.IOException;
import java.util.Set;

import com.ansj.vec.domain.WordEntry;

import me.xiaosheng.word2vec.Word2Vec;

public class ModelHandler {
	private String path;
	private Word2Vec vec = null;
	
	public ModelHandler(String path){
		this.path = path;
	}
	
	public void init() throws IOException{
		vec = new Word2Vec();
		vec.loadGoogleModel(path);
	}
	
	public Set<WordEntry> getSamWord(String word, int num){
		Set<WordEntry> similarWords = vec.getSimilarWords(word, num);
		for(WordEntry w : similarWords) {
			System.out.println(w.name + " : " + w.score);
		}
		return similarWords;
	}
}
