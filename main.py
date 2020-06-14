import requests
from multiprocessing import Pool
from time import sleep
from translate import eng as lang #choosing lang

good_proxy=[]

s=requests.Session()

headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:61.0) Gecko/20100101 Firefox/61.0',
'Accept': '*/*',
'Accept-Language':'ru-RU,ru;q=0.8,en-US'
}

def read_file(file):
	proxy_list=[]
	with open(file, 'r') as f:
		for i in f:
			i=i.replace('\n', '')
			proxy_list.append(i)
	return proxy_list	

def check_proxy(proxy):
	global good_proxy
	proxies = {
        "http": 'http://'+proxy,
        "https":'https://'+ proxy
    }
	try:
		s.get('https://duckduckgo.com', headers=headers, proxies=proxies)
		good_proxy.append(proxy)
		print(proxy+lang['good'])
	except requests.exceptions.ConnectionError:
		print(proxy+lang['bad'])
	sleep(1)
	return good_proxy
	
def write_txt(namefile, list_):
	with open(namefile, 'w') as f:
		for i in list_:
			for w in i:
				f.write(w+'\n')
				
def write_py(namefile, list_):
	with open(namefile, 'w') as f:
		f.write('[')
		for i in list_:
			for w in i:
				f.write(w+', ')
		f.write(']')
			
if __name__=='__main__':
	input_file=input(lang['input_file'])
	output_file=input(lang['output_file'])
	answer=input(lang['answer'])
	if answer=='y':
		name=input(lang['name'])
	answer=answer.lower()
	threads=int(input(lang['threads']))
	
	proxy_list=read_file(input_file)
	print(proxy_list)
	p = Pool(threads)
	a=p.map(check_proxy, proxy_list)
	write_txt(output_file, a)
	if answer=='y':
		write_py(name, a)
