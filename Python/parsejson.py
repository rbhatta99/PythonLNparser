import json
from datetime import datetime
from pprint import pprint
import re
import requests

def cleanhtml(raw_html):
  cleanr = re.compile('TEMPLATE\[(.*?)\]')
  cleantext = re.sub(cleanr, '', raw_html)

  return cleantext

def cleanhtml2(raw_data):
	cleanre=re.compile('&mdash;|&ndash')
	cleantext=re.sub(cleanre,'-',raw_data)
	return cleantext

i=0
#, encoding='utf-8'
newdata=[]
with open('wikipedia-dump.json',encoding="latin-1") as data_file:    
    data = data_file.readlines()

xmlstring='<?xml version="1.0" encoding="latin-1"?><sentences>'
# print (data.length)
for word in data:
	
	jsondata=json.loads(word)
	#print (jsondata['wid'])
	if 'templates' not in jsondata:
		pass
	else:
		
		#print i
		for key in jsondata['templates']:
			if key['name']=='date':
				
				#print (key['description'])
				try:
					date=datetime.strptime(str(key['description'][0]),'%B %d, %Y')
					if date>datetime(2015,1,1) and date<datetime(2015,12,31):
						print("\n\n\n")
						print (jsondata['wid'])
						paragraph=cleanhtml(jsondata['paragraphs'][0]).strip()
						paragraph=cleanhtml2(paragraph).strip()
						print("Current cleaned paragraph: "+paragraph+"\n\n")
						print("Current uncleaned paragraph: ")
						print(jsondata['paragraphs'][0])
						if(paragraph!=""):
							headers = {'Content-Type': 'application/json'}
							paragraph_json={'text':paragraph}
							print(paragraph_json)
							data=json.dumps(paragraph_json)
							r = requests.post('http://localhost:5000/process', data=data, headers=headers)
							parsetree=r.json()
							print (date)
							paragraph_parse=parsetree['sentences'][0]['parse']
							print(paragraph_parse)
							xmlstring=xmlstring+'<sentence date="'+date.strftime('%Y%m%d')+'" id="'+str(jsondata['wid'])+'" ><text>'+jsondata['title'][0]+'\n'+paragraph+'</text></sentence><parse>'+paragraph_parse+'</parse>'
							i=i+1		
							#print (date)
							newdata.append(word)
				except ValueError:
					pass
	

				
# print (newdata.length)
xmlstring=xmlstring+"</sentences>"
with open('newsxml.xml',"w",encoding="latin-1") as out:
	out.write(xmlstring)

with open('newwiki.json','w',encoding="utf-8") as outfile:
	json.dump(newdata,outfile)

print (i)



# print jsondata



	
    #json.load(data_file)


# parsed_json=json.loads("wikipedia-dump.json")
