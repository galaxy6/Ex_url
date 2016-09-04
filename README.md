
#Ex_url

##ex_url.py

Ex_url/1.0-dev -  automatic extract url tool using Search Engines

                  利用搜索引擎采集url的自动化工具。

##Introduce
1.系统环境kail,脚本环境python2.x

2.利用sublist3r的框架修改后做成的url采集工具，可对Baidu，Bing，Yahoo，Ask, Google,由于Google别屏蔽，用的反向代理，效果不是特别好。


##Installation

In Kail, you need to install some libraries.

splinter

phantomjs

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
