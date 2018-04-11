package cn.edu.fudan.se.MELink.util;

import java.util.List;

public class StringUtils {
	public static String link(List<String> list){
		StringBuilder sb = new StringBuilder();
		for(int i = 0; i < list.size()-1; i++)
			sb.append(list.get(i)).append(" ");
		if(list.size()>0)
			sb.append(list.get(list.size()-1));
		return sb.toString();
	}
}
