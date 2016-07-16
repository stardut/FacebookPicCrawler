#!/usr/bin/env python
# -*- coding:utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from cookielib import LWPCookieJar
import requests
import GetArg
import random
import os
import sys
import io
import time
import thread

#USER_ID = 100010625445795
USER_ID = 100010625445733
URL_PHOTO_ALBUM_FRONT = 'https://www.facebook.com/profile.php?id='
URL_PHOTO_ALBUM_END = '&sk=photos'
DOWNLOAD_PATH = 'D:\workspace\crawlerData\\facebook\\'


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

#function save_page
#	TODO->save html for debug
#	@param
#	page: content
#	name: file name
def save_page(page, name):
	file = open(LOCAL_PATH + name + 'test.html','w')
	file.write(page)
	file.close()

#function start
def start():	
	global s
	global USER_ID
	USER_ID = USER_ID - 1
	user_id = USER_ID
	url = URL_PHOTO_ALBUM_FRONT + str(user_id) + URL_PHOTO_ALBUM_END
	try:
		page = s.get(url = url, headers = headers, timeout = 10)
		soup = BeautifulSoup(page.content)
		divs = soup.findAll('div', attrs = {
			'class' : 'hidden_elem'
			})
		code_text = BeautifulSoup(divs[13].contents[0].contents[0])
		if code_text is None:
			print u'nonexistent user'
		else:
			links = code_text.findAll('a', attrs = {
				'class' : 'uiMediaThumb _6i9 uiMediaThumbMedium'
				})
			if links is None:
				print u'no public picture'
			else:
				for link in links:
					pic_page(user_id, link['href'])
	except Exception,e:
		print 'start error:',e

#function pic_page
#	TODO->get picture's link
#	@param:
#	user_id: download user id
#	link   : get picture's links page link	
def pic_page(user_id, link):
	time.sleep(0.2)
	global s
	try:
		page = s.get(url = link, headers = headers, timeout = 10)
		soup = BeautifulSoup(page.text)
		divs = soup.findAll('div',attrs = {
			'class' : 'hidden_elem'
			})
		a = BeautifulSoup(divs[3].contents[0].contents[0])
		pic_link = a.find('img', attrs = {'class' : '_46-i img'})['src']
		download_pic(pic_link, user_id)
	except Exception,e:
		print 'pic_page error:',e

#function download_pic
#	TODO->download picture
#	@param:
#	img_url : image's download url
#	user_id : download user id
def download_pic(img_url, user_id):
	download_path = DOWNLOAD_PATH + str(user_id)
	if not os.path.exists(download_path):
		os.mkdir(download_path)
	try:
		data = requests.get(img_url,timeout = 10, headers = headers).content
		fileName = str(int(time.time())) + '.jpg'
		filePath = download_path + '\\' + fileName
		image = open(filePath, 'wb')
		image.write(data)
		image.close()
		print u'Download Succeed:' , filePath
	except Exception,e:
		print "download_pic error: ",e

#function check_cookies
#	TODO->check cookies weather exist
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

#function login
#	TODO->login and save cookies into file
def login():
	login_params = {
		'email':USER_ACCOUNT,
		'pass':USER_PASSWORD
	}	
	login_page = s.get(URL_LOGIN)
	cookies = login_page.cookies
	try:
		login_res = s.post(url = URL_LOGIN,
						data = login_params,
						cookies = cookies,
						headers = headers,
						timeout = 10)
	except Exception,e:
		print 'login error:',e
	is_success = False
	print login_res
	if 1:   #TODO -> check login state (need complete)
		is_success = True
	else:
		is_success = False
		print 'get cookies fail'
	return is_success

#function crawl
#	TODO->start crawl data
#	@param
#	name : thread name
#	delay: delay time
def crawl(name,delay):
	global USER_ID
	while USER_ID > 0:		
		time.sleep(delay)
		start()

#function main
# TODO->create thread
def main():
	if check_cookies():
		print 'login success!'
		print 'start working...'
		try:
			thread.start_new_thread(crawl,('thread-1',0.1))
   			thread.start_new_thread(crawl,('thread-2',0.2))
   			thread.start_new_thread(crawl,('thread-3',0.3))
   			thread.start_new_thread(crawl,('thread-4',0.4))   		
   		except Exception,e:
   			print 'thread error:',e
   		crawle('main',0.5)
	else:
		print 'login fail.please check your user and password!'
		print 'Maybe solve: --> delete the ' + COOKIES_FILE + ' and then try again.'

if __name__ == '__main__':
	main()
