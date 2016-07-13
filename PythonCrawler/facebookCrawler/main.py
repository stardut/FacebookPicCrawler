#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import GetArg
import random
import os
from cookielib import LWPCookieJar

USER_ID = 100010625445795
URL_PHOTO_ALBUM_FRONT = 'https://www.facebook.com/profile.php?id='
URL_PHOTO_ALBUM_END = '&sk=photos'


USER_ACCOUNT = '277907260@qq.com'
USER_PASSWORD = 'a12jk12jk'
URL_LOGIN = 'https://www.facebook.com/login.php?login_attempt=1&lwv=100'
LOCAL_PATH = 'D:\workspace\Python\PythonCrawler\PythonCrawler\\facebookCrawler\\'
COOKIES_FILE = LOCAL_PATH + 'cookies'

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

s = requests.Session()
s.headers.update(headers)
s.cookies = LWPCookieJar(COOKIES_FILE)

def save_page(page):
	file = open(LOCAL_PATH + 'test.html','w')
	file.write(page)
	file.close()

def start():
	global s
	global USER_ID
	USER_ID = USER_ID - 1
	print u'正在下载用户ID为 ' + str(USER_ID) + u' 的数据'
	url = URL_PHOTO_ALBUM_FRONT + str(USER_ID) + URL_PHOTO_ALBUM_END
	try:
		page = s.get(url = url,headers = headers)
		soup = BeautifulSoup(page.text)
		print soup

		divs = soup.find('div',attrs = {
			'id' : 'u_0_2e'
			})
		print divs
		if divs is None:
			print u'该用户没有公开图片'
		else:
			for div in divs:
				link = div.find('a',attrs = {'class' : 'uiMediaThumb _6i9 uiMediaThumbMedium'})
				pic_page(link['href'])
		save_page(soup)
	except Exception,e:
		print 'start error:',e


def pic_page(link):
	print link
	pass


# 登录并保存 cookie 到文件
# "从 cookie 文件加载上次的 cookie，这样就不需要重复登陆"
def check_cookies():
	print 'begining...'
	if not os.path.exists(COOKIES_FILE):
		if login():
			return True
		else:
			return False
	else:
		s.cookies.load()
		print 'load cookies success'
		return True


#	login
#	save and load cookies
def login():

	login_params = {
		'email':USER_ACCOUNT,
		'pass':USER_PASSWORD
	}
	
	login_page = s.get(URL_LOGIN)
	cookies = login_page.cookies
	login_res = s.post(url = URL_LOGIN,
					data = login_params,
					cookies = cookies,
					headers = headers,
					timeout = 10)
	is_success = False
	print login_res
	#save_page(login_res)
	if 1:
		#s.cookies.save()
		is_success = True
	else:
		is_success = False
		print 'get cookies fail'
	return is_success

def main():
	if check_cookies():
		print 'login success!'
		print 'start working...'
		start()
	else:
		print 'login fail.please check your user and password!'
		print 'Maybe solve: --> delete the ' + COOKIES_FILE + ' and then try again.'



if __name__ == '__main__':
	main()
