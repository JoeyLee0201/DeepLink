package cn.edu.fudan.se.MELink.nlp;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.regex.Pattern;

import org.eclipse.jgit.revwalk.RevCommit;

import cn.edu.fudan.se.MELink.util.StringUtils;
import cn.edu.fudan.se.MELink.util.Words;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class StandfordParser {
    private static Pattern noWordPattern=Pattern.compile(".*[a-zA-Z]+.*");
    private static Pattern websitePattern=Pattern.compile("(((https|http)?://)?([a-z0-9]+[.])|(www.))\\w+[.|\\/]([a-z0-9]{0,})?[[.]([a-z0-9]{0,})]+((/[\\S&&[^,;\u4E00-\u9FA5]]+)+)?([.][a-z0-9]{0,}+|/?)");
    
	private static Properties props = new Properties();
	static{
        props.put("annotators", "tokenize, ssplit, pos, lemma");  
	}
	private static StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
	
	public static List<String> parse(String s){
		List<String> result = new ArrayList<String>();
		
		Annotation document = new Annotation(s);
        pipeline.annotate(document);
        
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        for(CoreMap sentence: sentences) {
        	// one sequence
        	for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
        	    String lemma = token.lemma().toLowerCase();
        	    if(!needDelete(lemma) && !needDelete(token.originalText().toLowerCase())){
                	result.add(lemma);
                }
        	}
        }
        return result;
	}
	
	public static void parseCommit(RevCommit commit, BufferedWriter bw){
		String s = commit.getFullMessage();
		Annotation document = new Annotation(s);
        pipeline.annotate(document);
        
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        for(CoreMap sentence: sentences) {
        	// one sequence
    		List<String> result = new ArrayList<String>();
        	for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
        	    String lemma = token.lemma().toLowerCase();
        	    if(!needDelete(lemma) && !needDelete(token.originalText().toLowerCase())){
                	result.add(lemma);
                }
        	}
        	try {
				bw.write(StringUtils.link(result));
				bw.write("\n");
			} catch (IOException e) {
				e.printStackTrace();
			}
        }
	}
	
	private static boolean needDelete(String s){
		// delete short
//		if(s==null||s.length()<3) return true;
		// delete stop words 
		if(Words.STOP_WORD.contains(s)) return true;
		// delete no word 
		if(!noWordPattern.matcher(s).matches()) return true;
		// delete no word 
		if(websitePattern.matcher(s).matches()) return true;
		return false;
	}
}
