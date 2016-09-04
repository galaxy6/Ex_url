
#Ex_url

##ex_url.py

Ex_url/1.0-dev -  automatic extract url tool using Search Engines

利用搜索引擎采集url的自动化工具。

##Introduce
1.系统环境kail,脚本环境python2.x

2.利用sublist3r的框架修改后做成的url采集工具，可对Baidu，Bing，Yahoo，Ask, Google,由于Google被屏蔽，用的反向代理，效果不是特别好。


##Installation

In Kail, you need to install some libraries.

splinter

phantomjs

##Examples

        采集域名为百度的信息并显示详细信息,利用的搜索引擎不设置时是使用全部
        root@kali:/search_url/test# python ex_url.py -d site:baidu.com -v

        利用百度搜索采集链接中带test.ph?id关键词额URL并显示详细信息
        root@kali:/search_url/test# python ex_url.py -d inurl:test.php?id -e baidu -

        利用百度搜索引擎采集搜索关键词为site:xxx.com.cn+inurl:orderby的URL,采取的数量为30条，并显示信息信息
        root@kali:/search_url/test# python ex_url.py -d site:xxx.com.cn+inurl:orderby -e baidu -n 30 -v

        把采集的URL链接信息存在test.txt文件中
        root@kali:/search_url/test# python ex_url.py -d site:xxx.com.cn+inurl:orderby -e yahoo -n 30 -v -o test.txt



##Usage
    usage: ex_url.py [-h] -d COMMAND [-e ENGINE] [-v [VERBOSE]] [-n NUMBER] [-o OUTPUT]
    
    OPTIONS:
    
      -h, --help            show this help message and exit
      
      -d COMMAND, --command COMMAND     command name to enumrate it's urls
      
      -e ENGINE, --engine ENGINE        engine name
      
      -v [VERBOSE], --verbose [VERBOSE] display results in realtime
      
      -n NUMBER, --number NUMBER        get the number of links
      
      -o OUTPUT, --output OUTPUT        save the results to text file
     
      Example: python ex_url.py -d site:baidu.com


注：本工具仅作为安全测试工具，请勿用户非法用途。
