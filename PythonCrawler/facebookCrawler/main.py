#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import GetArg
import random
from cookielib import LWPCookieJar

USER_ACCOUNT = '277907260@qq.com'
USER_PASSWORD = 'a12jk12jk'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2763.0 Safari/537.36',
    'Cache-Control':'max-age=0',
    'Accept-Encoding':'gzip, deflate',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests':'1',
    'content-type':'application/x-www-form-urlencoded',
    'origin':'https://www.facebook.com',
    'referer':'https://www.facebook.com/login',
    'authority':'www.facebook.com',
    'accept-language':'zh-CN,zh;q=0.8'
}

def login():
	login_params = {
		'email':USER_ACCOUNT,
		'pass':USER_PASSWORD
	}
	s = requests.Session()
	login_page = s.get('https://www.facebook.com/login.php?login_attempt=1&lwv=100')
	cookies = login_page.cookies
	login_res = s.post('https://www.facebook.com/login.php?login_attempt=1&lwv=100',
			data = login_params,
			headers = headers,
			cookies = cookies,
			timeout = 10)
	print login_res
	file = open('D:\workspace\Python\PythonCrawler\PythonCrawler\\facebookCrawler\\test.html','w')
	file.write(login_res.content)
	file.close()
	return 1

def main():
	if login():
		print 'login success!'
		print 'start working...'
		pass
	else:
		print 'login fail.please check your user and password!'



if __name__ == '__main__':
	main()
