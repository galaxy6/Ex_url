


automatic extract url tool using Search Engines


Installation

In Kail, you need to install some libraries.

You can use pip or easy_install or apt-get to do this.

splinter
phantomjs


usage: ex_url.py [-h] -d COMMAND [-e ENGINE] [-v [VERBOSE]] [-n NUMBER]
                 [-o OUTPUT]

OPTIONS:
  -h, --help            show this help message and exit
  -d COMMAND, --command COMMAND
                        command name to enumrate it's urls
  -e ENGINE, --engine ENGINE
                        engine name
  -v [VERBOSE], --verbose [VERBOSE]
                        display results in realtime
  -n NUMBER, --number NUMBER
                        get the number of links
  -o OUTPUT, --output OUTPUT
                        save the results to text file

Example: python ex_url.py -d site:baidu.com


本工具仅作为安全测试工具，请勿用户非法用途。