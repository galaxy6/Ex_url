#!/usr/bin/env python
#_*_coding:utf-8_*_

import re
import sys
import os
import argparse
import time
import requests
import urlparse
import urllib
import random
import multiprocessing
import threading
import logging
from splinter import Browser
try:
	import requests.packages.urllib3
	requests.packages.urllib3.disable_warnings()
except:
    pass

#Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

#Console Colors
if is_windows:
	G = Y = B = R = W = G = Y = B = R = W = '' #use no terminal colors on windows
else:
	G = '\033[92m' #green
	Y = '\033[93m' #yellow
	B = '\033[94m' #blue
	R = '\033[91m' #red
	W = '\033[0m'  #white

def banner():
    print """%s

    Ex_url/1.0-dev -  automatic extract url tool using Search Engines
    
    """%(Y)

def parser_error(errmsg):
    banner()
    print "Usage: python "+sys.argv[0]+" [Options] use -h for help"
    print R+"Error: "+errmsg+W
    sys.exit()

def parse_args():
    #parse the arguments
    parser = argparse.ArgumentParser(epilog = '\tExample: \r\npython '+sys.argv[0]+" -d site:baidu.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--command', help="command name to enumrate it's urls", required=True)
    parser.add_argument('-e', '--engine', help="engine name", required=False)
    parser.add_argument('-v', '--verbose', help='display results in realtime', nargs='?', default=False)
    parser.add_argument('-n', '--number',help='get the number of links', default=40)
    parser.add_argument('-o', '--output', help='save the results to text file')
    return parser.parse_args()
 
def log_file():
    #运行日志,需要调试式开启
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',filename='./test.log')
    return

def write_file(filename, urls):
    #saving subdomains results to output file
    print "%s[-] Saving results to file: %s%s%s%s"%(Y,W,R,filename,W)
    with open(str(filename), 'wb') as f:
        for url in urls:
            f.write(url+"\r\n")

def remove_similar_url(index):
    #去重
    url_param = urlparse.urlparse(index)
    path_query = "%s?%s" % (url_param.path,url_param.query)
    p = re.compile(r'\d+')
    url_re = p.sub(r'd+',path_query)
    url_pattern = "http://%s%s" % (url_param.netloc,url_re)
    return url_pattern

class enumratorBase(object):
    def __init__(self, base_url, engine_name, command):
        self.session = requests.Session()
        self.command = command
        self.timeout = 10
        self.base_url = base_url
        self.engine_name = engine_name
        self.print_banner()

    def print_banner(self):
        print G+"[-] Searching now in %s.." %(self.engine_name)+W
        return

    def send_req(self, query, page_no=1):
       
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
        }
        
        url =  self.base_url.format(query=query, page_no=page_no)
        #logging.info('%s is had been requset...' % url)
        try:
            resp = self.session.get(url, headers=headers, timeout=self.timeout)
        except Exception as e:
            raise
        return self.get_response(resp)

    def get_response(self,response):
        if hasattr(response, "text"):
	        return response.text
        else:
            return response.content

	def end_while(self,resp):
		""" child class should end the application """
		return
			
	#Override
    def extract_commands(self, resp):
        """ chlid class should override this function """
        return

    #Override
    def check_response_errors(self, resp):
        """ chlid class should override this function
        The function should return True if there are no errors and False otherwise
        """
        return True

    def should_sleep(self):
        """Some enumrators require sleeping to avoid bot detections like Google enumerator"""
        return

    def generate_query(self):
        """ chlid class should override this function """
        return

    def get_number(self):
        """get the number of links"""
        return

    def get_page(self, num):
        """ chlid class that user different pagnation counter should override this function """
        return num + 10

    def enumerate(self):
        flag = True
        page_no = 0
        links = []
        while flag:
            query = self.generate_query()
            resp = self.send_req(query, page_no)
			
            if True:
                page_no = self.get_page(page_no)
                count = int(self.get_number())
                if page_no > count:
                    break

            #check if there is any error occured

            if not self.check_response_errors(resp):
                break

            link = self.extract_commands(resp)
            links.extend(link)
            self.should_sleep()
            
            if not self.end_while(resp):
                break
        return links


class enumratorBaseThreaded(multiprocessing.Process, enumratorBase):
    def __init__(self, base_url, engine_name, command, q=None, lock=threading.Lock()):
        enumratorBase.__init__(self, base_url, engine_name, command)
        multiprocessing.Process.__init__(self)
        self.lock = lock
        self.q = q
        return

    def run(self):
        command_list = self.enumerate()
        self.q.put(command_list)
        logging.debug('%s %s' %(self.engine_name,self.base_url))

class GoogleEnum(enumratorBaseThreaded):
    def __init__(self, command, verbose, number, q=None):
        self.verbose = verbose
        self.number = number
        base_url = "https://www.meiguge.com/#q={query}&start={page_no}"
        self.engine_name = "Google"
        enumratorBaseThreaded.__init__(self, base_url, self.engine_name, command, q=q)
        self.q = q
        return

    def extract_commands(self, resp):
        link_list = []
        link_regx = re.compile('<cite.*?>(.*?)<\/cite>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                if not link.startswith('http'):
                    link="http://"+link
                    link_list.append(link)
                if self.verbose:
                    print "%s%s: %s%s"%(R, self.engine_name, W, link)
        except Exception as e:
            pass
        return link_list

    def check_response_errors(self, resp):
        if 'Our systems have detected unusual traffic' in resp:
            print R+"[!] Error: Google probably now is blocking our requests"+W
            print R+"[~] Finished now the Google Enumeration ..."+W
            return False
        return True

    def should_sleep(self):
        time.sleep(random.randint(1,3))
        return
    
    def get_number(self):
        return self.number if self.number else 40

    def generate_query(self):
        query = "{command} ".format(command=self.command)
        return query

    def end_while(self,resp):
        pattern = re.compile('id="pnnext"')
        result = pattern.findall(resp)
        if result:
            return True
  
    def send_req(self,query,page_no=1):
        url = self.base_url.format(query=query,page_no=page_no)
        try:
            browser = Browser('phantomjs')
            browser.visit(url)
            resp = browser.html
        except Exception as e:
            raise
        return resp

class YahooEnum(enumratorBaseThreaded):
    def __init__(self, command, verbose, number, q=None):
        base_url = "https://search.yahoo.com/search?p={query}&b={page_no}"
        self.engine_name = "Yahoo"
        enumratorBaseThreaded.__init__(self, base_url, self.engine_name, command, q=q)
        self.verbose  = verbose
        self.number = number
        self.q = q
        return

    def extract_commands(self, resp):
        link_regx = re.compile('<a class=" ac-algo ac-\d+th lh-\d+".*?href="(.*?)"')
        try:
            links = link_regx.findall(resp)
            for link in links:
                    if self.verbose:
                       print "%s%s: %s%s"%(R, self.engine_name, W, link)
        except Exception as e:
            pass

        return links

    def should_sleep(self):
        time.sleep(random.randint(1,2))
        return

    def get_number(self):
        return self.number if self.number else 40

    def generate_query(self):
        query = "{command}".format(command=self.command)
        return query
    
    def end_while(self,resp):
        pattern = re.compile('<a class="next" href=".*?">Next</a>')
        result = pattern.findall(resp)
        if result:
            return True
   
    def send_req(self, query, page_no=1):
        url =  self.base_url.format(query=query, page_no=page_no)

        try:
            browser = Browser('phantomjs')
            browser.visit(url)
            resp = browser.html
            browser.quit()
        except Exception as e:
            print e
            raise
       
        return resp

class AskEnum(enumratorBaseThreaded):
    def __init__(self, command, verbose, number, q=None):

        base_url = 'http://www.ask.com/web?q={query}&page={page_no}&qid=8D6EE6BF52E0C04527E51F64F22C4534&o=0&l=dir&qsrc=998&qo=pagination'
        self.engine_name = "Ask"
        enumratorBaseThreaded.__init__(self, base_url, self.engine_name, command,  q=q)
        self.verbose = verbose
        self.number = number
        self.q = q
        return

    def extract_commands(self, resp):
        link_regx = re.compile('<a class="web-result-title-link" href="(.*?)"')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                    if self.verbose:
                        print "%s%s: %s%s"%(R, self.engine_name, W, link)
        except Exception as e:
            pass

        return links_list

    def should_sleep(self):
        time.sleep(random.randint(1,2))
        return 
    
    def get_number(self):
        return self.number if self.number else 40

    def end_while(self,resp):
        pattern =re.compile('<li class="pagination-next">Next</li>')
        result = pattern.findall(resp)
        if result:
            return True


    def generate_query(self):
        query = "{command} ".format(command=self.command)
        return query

class BingEnum(enumratorBaseThreaded):
    def __init__(self, command, verbose, number, q=None):
        base_url = 'http://cn.bing.com/search?q={query}&go=Submit&first={page_no}'
        self.engine_name = "Bing"
        enumratorBaseThreaded.__init__(self, base_url, self.engine_name,command, q=q)
        self.verbose = verbose
        self.number = number
        self.q = q
        return

    def extract_commands(self, resp):
        link_regx = re.compile('"><h2><a target="_blank" href="(.*?)"')

        try:
            links = link_regx.findall(resp)
            for link in links:
                    if self.verbose:
                        print "%s%s: %s%s"%(R, self.engine_name, W, link)
        except Exception as e:
            pass
        return links
	
    def should_sleep(self):
        time.sleep(random.randint(1,2))

    def get_number(self):
        return self.number if self.number else 40       

    def end_while(self,resp):
        pattern =re.compile('<div class="sw_next">')
        result = pattern.findall(resp)
        if result:
            return True

    def generate_query(self):
        query = "{command} ".format(command=self.command)
        return query

class BaiduEnum(enumratorBaseThreaded):
   
    def __init__(self, command, verbose, number , q=None):
        
        base_url = 'https://www.baidu.com/s?pn={page_no}&wd={query}&oq={query}'
        self.engine_name = "Baidu"
        self.verbose = verbose
        self.number = number
        enumratorBaseThreaded.__init__(self, base_url, self.engine_name, command, q=q)
        self.q = q
        return


    def extract_commands(self, resp):
        link_list = []
        link_regx = re.compile('<a target="_blank" href="(.*?)" class="c-showurl" style="text-decoration:none;">')
        try:
            links = link_regx.findall(resp)
            for link in links:
                url_ = self.decode_url(link)
                if url_:
                    link_list.append(url_)
                if self.verbose:
                    print "%s%s: %s%s"%(R, self.engine_name, W, url_)
             
        except Exception as e:
            pass
        return link_list

    def get_number(self):
        return self.number if self.number else 40

    def should_sleep(self):
    	time.sleep(random.randint(1, 2))
        return

    def generate_query(self):
        query = "{command}".format(command=self.command)
        return query
    def end_while(self,resp):
       	pattern = re.compile('\d+</span></strong><a href=')
        result = pattern.findall(resp)
        if result:
            return True

    def decode_url(self,url):
        try:
            req = requests.get(url,allow_redirects=True)
            return req.url
        except Exception as e:
            pass

def main():
    args = parse_args()
    command = args.command
    savefile = args.output
    engine = args.engine
    number = args.number
    google_list = []
    bing_list = []
    baidu_list = []
    urls = []
    links_pattern = []
    urls_queue = multiprocessing.Queue()

   
    #Check Verbosity
    global verbose
    verbose = args.verbose
    if verbose or verbose is None:
        verbose = True

    #Print the Banner
    banner()
    #log_file()
    print B+"[-] Enumerating command now for %s"% command +W

    if verbose:
        print Y+"[-] verbosity is enabled, will show the command results in realtime"+W 


    if(engine =='baidu' or engine =='google' or engine =='bing' or engine=='yahoo' or engine=='ask'):
        if(engine == 'baidu'):
            enum = BaiduEnum(command,verbose,number,q=urls_queue)
        elif(engine == 'google'):
            enum = GoogleEnum(command,verbose,number,q=urls_queue)
        elif(engine == 'bing'):
            enum = BingEnum(command,verbose,number,q=urls_queue)
        elif(engine == 'yahoo'):
            enum = YahooEnum(command,verbose,number,q=urls_queue)
        elif(engine == 'ask'):
            enum = AskEnum(command,verbose,number,q=urls_queue)
        else:
            print '[-] Engine name not find!!!'
        enum.start()
        enum.join()
    else:
        enums = [enum(command, verbose, number, q=urls_queue) for enum in BaiduEnum,BingEnum,YahooEnum,GoogleEnum,AskEnum]
        for enum in enums:
            enum.start()
        for enum in enums:
            enum.join()

		


    search_list = set()
    while not urls_queue.empty():
        search_list= search_list.union(urls_queue.get())
 	
    for url in search_list:
        url_ = remove_similar_url(url)
        if url_ not in links_pattern:
            links_pattern.append(url_)
            urls.append(url)


    if urls:
       if savefile:
            write_file(savefile, search_list)
       print Y + "[-] Total Unique urls Found: %s"% len(urls) + W
       for u in urls:
            print G+u+W
          

if __name__=="__main__":
    main()
