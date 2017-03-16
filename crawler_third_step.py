# Author:Haozhen Liu
# # -*- coding: utf-8 -*-

# import sys;
# reload(sys);
# sys.setdefaultencoding("utf-8");

import requests;
import csv;
import re;
import json;
import time;

def main():

	# 存储所有的journal信息
	journal_ai=[];
	with open("journal_id_name_ai.csv","rb") as ft:
		reader=csv.reader(ft);
		for row in reader:
			if row[0]!="ID":
				journal_ai.append(row[1]);

	# 存储每篇被引用文章的id
	paper_id=[];
	with open("papers_journal_of_machine_learning_research_modify.csv","rb") as ft:
		reader=csv.reader(ft);
		for row in reader:
			if row[0]!="ID":
				paper_id.append(row[0]);
	
	# 对每一篇文章做处理，找到对应的参考文献
	headers = {'Accept':'application/json'};
	str1="http://api.elsevier.com/content/abstract/EID:";
	str2="?apikey=ab6a63d43253501662ea07c589c6c0a8&view=REF";

	paper_total=[];
	first_row=["P_ID","R_ID","Journal","Author"];
	paper_total.append(first_row);

	count=1;
	for eid in paper_id:
		# 打印每篇文章id
		url_paper=str1+eid+str2;
		time.sleep(10);
		page_response=requests.get(url_paper, headers=headers);
		print (page_response);
		page=json.loads(page_response.content.decode("utf-8"));

		# 安全检查
		if page==None or page.has_key('abstracts-retrieval-response')==False:
			continue;

		if page['abstracts-retrieval-response']==None or page['abstracts-retrieval-response'].has_key('references')==False:
			continue;

		if page['abstracts-retrieval-response']['references']==None or page['abstracts-retrieval-response']['references'].has_key('reference')==False:
			continue;

		# 解析得到结果
		for paper in page['abstracts-retrieval-response']['references']['reference']:
			sourcetitle=paper['sourcetitle'];
			if sourcetitle==None: # 没有期刊
				continue;

			journal_paper="";
			# 对期刊进行严格判断
			for journal in journal_ai:
				if journal in sourcetitle and "conference" not in sourcetitle:
					if journal=="Artificial Intelligence" and "Artificial Intelligence in Medicine" in sourcetitle:
						journal_paper="Artificial Intelligence in Medicine";
						break;
					elif journal=="Artificial Intelligence" and "Engineering Applications of Artificial Intelligence" in sourcetitle:
						journal_paper="Engineering Applications of Artificial Intelligence";
						break;
					elif journal=="Artificial Intelligence" and "International Journal of Pattern Recognition and Artificial Intelligence" in sourcetitle:
						journal_paper="International Journal of Pattern Recognition and Artificial Intelligence";
						break;
					elif journal=="Artificial Intelligence" and "Journal of Experimental and Theoretical Artificial Intelligence" in sourcetitle:
						journal_paper="Journal of Experimental and Theoretical Artificial Intelligence";
						break;
					elif journal=="Machine Learning" and "Journal of Machine Learning Research" in sourcetitle:
						journal_paper="Journal of Machine Learning Research";
						break;
					elif journal=="Evolutionary Computation" and "IEEE Transactions on Evolutionary Computation" in sourcetitle:
						journal_paper="IEEE Transactions on Evolutionary Computation";
						break;
					elif journal=="Pattern Recognition" and "International Journal of Pattern Recognition and Artificial Intelligence" in sourcetitle:
						journal_paper="International Journal of Pattern Recognition and Artificial Intelligence";
						break;
					elif journal=="Pattern Recognition" and "Pattern Recognition Letters" in sourcetitle:
						journal_paper="Pattern Recognition Letters";
						break;
					elif journal=="Computational Intelligence" and "International Journal of Computational Intelligence and Applications" in sourcetitle:
						journal_paper="International Journal of Computational Intelligence and Applications";
						break;
					else:
						journal_paper=journal;
						break;


			if journal_paper=="": #没有找到期刊
				continue;
			
			if paper['author-list']==None:#没有作者
				continue;

			temp_author=[];
			for element in paper['author-list']['author']:
				if element.has_key('ce:given-name'):
					temp_author.append(element['ce:given-name']+" "+element['ce:surname']);
				else:
					temp_author.append(element['ce:indexed-name']);
			temp=[];
			temp.append(eid);#存入文章id
			temp.append(paper['scopus-eid']);#存入参考文献id
			temp.append(journal_paper);#存入参考文献所在期刊
			temp.extend(temp_author);
			paper_total.append(temp);

		print (count,eid);
		count=count+1;

	# 保存参考文献
	with open("paper_reference_journal_of_machine_learning_research.csv","wb") as ft:
		writer=csv.writer(ft);
		for x in paper_total:
			writer.writerow(x);


if __name__ == '__main__':
	main();