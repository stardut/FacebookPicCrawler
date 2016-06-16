#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from cookielib import LWPCookieJar
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import os
import sys
import time
import re
import cookielib
import requests
import string
import MySQLdb
import urllib2
import Queue
import random
import GetArg


#mixi网站的编码为 euc-jp
reload(sys)
sys.setdefaultencoding('euc-jp')

#已经下载好的用户数
_id = 748

user_home_url = 'http://mixi.jp/show_friend.pl?id='
pic_url = 'http://mixi.jp/list_album.pl?id='


#登录的账号和密码，还有出生年月-->密保的验证
account = 'ranjun4366@gmail.com'
password = 'a12jk12jk'
birth_year = '1995'
birth_mon = '9'
birth_day = '22'

#数据库的各项参数,需要建立一个名为test的表
'''
create table test(
	id char(8) not null,
	sex char(8),
	name char(30),
	address char(50),
	birthday char(20),
	birthplace char(50),
	age char(15),
	album smallint,
	photo smallint,
	primary key (id)
	);
'''

localhost = '127.0.0.1'
db_user = 'root'
db_password = 'a12jk12jk'
db_name = 'image_info'

#建立数据库连接
db = MySQLdb.connect(localhost, db_user, db_password, db_name)
cursor = db.cursor()

#连接太少会报 max tries 异常
'''
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False
'''
#访问头
headers = {
    'User-Agent':'',
    'Host':'mixi.jp',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer':'https://mixi.jp/login.pl?from=login1',
    'Upgrade-Insecure-Requests':'1'
}

'''
	获得动态ip, 网址中的 num 代表此次运行从ip代理商那里取得的ip数目。
	这是我在网上买的代理ip，但是非常不稳定
'''
arg = GetArg.GetArg()
#proxies = arg.getIP('http://qsrdk.daili666api.com/ip/?tid=559798042875697&num=40&category=2')
proxies = [{'http' : 'http://36.41.123.213:26837'},{'http':'111.72.82.77:55741'}]
#proxies = ['1']
ip_len = len(proxies)


#下载并保存图片
def download_pic(_id, img_url, load_path, proxy):
	time.sleep(0)
	try:
		#data = requests.get(img_url, proxies = proxy).content
		data = requests.get(img_url,timeout = 10).content
		fileName = bytes(_id) + '.jpg'
		filePath = load_path + fileName
		image = open(filePath, 'wb')
		image.write(data)
		image.close()
		print u'\n图片下载成功,已保存在' + filePath
	except Exception,e:
		print "download_pic error: ",e

#开始执行抓取任务：图片和个人信息
def start( _id):
	time.sleep(0)
	global cookies
	proxy = {}
	#模拟浏览器
	agent_num = int(random.random() * 170) % 17
	ip_num = int(random.random() * ip_len * 100) % ip_len
	headers['User-Agent'] = arg.getAgent(agent_num)
	#设置动态ip
	proxy['http'] = proxies[ip_num]
	proxy['https'] = proxies[ip_num]	
	if check_id_album(_id) > 0:
		print u"\n正在下载用户ID为 %s 的数据..." % str(_id)
		album_count, public = handle_pic(_id, proxy)
		'''
		if album_count > -1:
			handle_info( _id, album_count, public, proxy)
		'''

#抓取user相册
def handle_pic(_id, proxy):
	public = 0
	time.sleep(0)
	global cookies	
	links = []
	album_count = 0
	photo_url = pic_url + str(_id)
	try:
		html = requests.get(photo_url, cookies = cookies, headers = headers, timeout = 10)
		#html = requests.get(photo_url, cookies = cookies, headers = headers, timeout = 10, proxies = proxy)

		file = open('D:\pythonSpider\mycode\data.html','w')
		file.write(html.content)
		file.close()
		soup = BeautifulSoup(html.text)
		div = soup.find('div', attrs = {'class' : 'leftbox'})
		if  div is None:
			print u"\n用户不存在 id：%s" % str(_id)
			return -1,0
		else:
			leftbox = div.find_all('tr')
			if leftbox is not None:
				for row in leftbox:
					album_count = int(album_count) + 1
					link = row.find('a')
					links.append('http://mixi.jp/' + link['href']) #补全连接
				public = handle_url(links, _id, proxy)  #爬取图片此处需要取消注释
				return album_count,public
			else:
				return 0, public
	except Exception, e:
		print u'抓取出错'
		print 'handle_pic is error:',e
		return -2,public
	

#抓取每个相册中每一页图片的 url
def handle_url(links, _id, proxy):
	public = 0
	time.sleep(0)
	global cookies
	#判断是否可以为公开相册
	try:
		for link in links:
			time.sleep(0)
			#print link.encode('gbk')
			#检查是否为公开相册
			check = requests.get(link, cookies = cookies, headers = headers, timeout = 10)
			#check = requests.get(link, cookies = cookies, headers = headers, timeout = 10, proxies = proxy)
			soup = BeautifulSoup(check.text)
			if soup.find('div', attrs = {'class' : 'leftbox'}) is None:
				continue
			else:
				public = int(public) + 1;				
				#第一页直接抓取放大图片的url
				handle_pic_url( link, _id, proxy)
				#之后每一页分别抓取
				#html = requests.get(link, cookies = cookies, headers = headers,  timeout = 10, proxies = proxy)
				html = requests.get(link, cookies = cookies, headers = headers,  timeout = 10)

				soup = BeautifulSoup(html.text)
				page_list = soup.find('div', attrs = {'class' : 'pagetext_top inlineList'})
				if page_list is not None:
					pages = page_list.find_all('a')
					for page in pages:
						link = page['href']
						handle_pic_url( 'http://mixi.jp/' + link, _id, proxy)
		return public
	except Exception, e:
		print 'handle_url is error: ', e
		return public

#抓取每一页图片的放大的url
def handle_pic_url(url, _id, proxy):
	time.sleep(0)
	global cookies
	try:
		html = requests.get(url, cookies = cookies, headers = headers,  timeout = 10)
		#html = requests.get(url, cookies = cookies, headers = headers,  timeout = 10, proxies = proxy)
		soup = BeautifulSoup(html.text)
		divs = soup.find_all('div', attrs = {'class' : 'thumbnail'})
		for div in divs:
			nodes = div.find_all('a')
			if nodes is not None:
				for node in nodes:	
					link = 'http://mixi.jp/' + node['href']
					handle_pic_download_url( link, _id, proxy)
	except Exception, e:
		print 'handle_pic_url is error: ', e

#获取每个图片的下载url
def handle_pic_download_url(url, _id, proxy):
	global cookies
	time.sleep(18)
	try:
		#html = requests.get(url, cookies = cookies, headers = headers, timeout = 10, proxies = proxy)
		html = requests.get(url, cookies = cookies, headers = headers, timeout = 10)
		soup = BeautifulSoup(html.text)
		img = soup.find('img', attrs = {'alt' : 'photo'})
		link = img['src']
		load_path = 'D:\pythonSpider\data\photo\\' + str(_id)
		pic_name = int(time.time())
		if not os.path.exists(load_path):
			os.makedirs(load_path)
		download_pic(pic_name, link, load_path + '\\', proxy)
	except Exception, e:
		print 'handle_pic_download_url is error:',e

#抓取user信息: 个人基本信息，个人头像
def handle_info(_id, album_count, public, proxy):
	time.sleep(0)
	global cookies
	#抓取个人信息
	data = {
		'id' : str(_id),
		'name' : '',
		'sex' : '',
		'address' : '',
		'birthday' : '',
		'birthplace' : '',
		'age' : '',
		'public' : int(public),
		'album': int(album_count)
	}

	#获取个人详细信息
	'''
	try:
		home_url = user_home_url + str(_id)
		html = requests.get(home_url, cookies = cookies, headers  = headers, timeout = 10, proxies = proxy)
		soup = BeautifulSoup(html.text)
		div = soup.find('div', attrs = {'class' : 'profileListTable'})
		for info in div.find_all('tr'):
			if info.th.string is not None and info.td.string is not None:
				(key, value) = fix_data(_id, info.th.string.encode('utf-8'), info.td.string.encode('utf-8'))
				data[key] = value
	except Exception,e:
		print 'handle_info.html',e
	'''
	insert_database(data)
	#抓取个人头像
	'''
	try:
		img = soup.find('p', attrs = {'class' : 'photo'})
		link = img.find('img')
		if not os.path.exists('D:\pythonSpider\data\portrait'):
			os.makedirs('D:\pythonSpider\data\portrait')
		download_pic(_id, link['src'], 'D:\pythonSpider\data\portrait\img', proxy)
	except Exception,e:
		print 'handle_info.img',e
	'''

#将user信息插入到数据库
def insert_database(data):
	'''
	sql = "insert into test(id, sex, name, address, birthday, birthplace, age, album) \
		value('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
		(data['id'], data['sex'], data['name'], data['address'], \
			data['birthday'], data['birthplace'], data['age'], data['album'])
	'''
	sql = "insert into ID(id, album, public)value('%s', %d, %d)" % (data['id'], data['album'], data['public'])
	try:
		cursor.execute(sql)
		db.commit()
		print u"\nID %s 的用户数据保存成功" % (data['id'])
	except Exception, e:
		print 'insert_database error:',e

#检查该id是否存在相册
def check_id_album(_id):
	sql = "select public from id where id=%d" % (int(_id))
	try:
		cursor.execute(sql)
		result = cursor.fetchall()
		#print result[0]
		if result[0] != None:
			return result[0][0]
		else:
			return 0;
	except Exception, e:
		print _id ,'--> check_id_album: ',e

#整理数据
def fix_data(_id, key, value):
	if key == '名前':
		key = 'name'
		value = value.replace(' ','')
		value = value.replace('\n','')
		return key,value
	if key == '性別':
		key = 'sex'
		value = value.replace(' ','')		
		value = value.replace('\n','')
		return key,value
	if key == '年齢':
		key = 'age'
		value = value.replace(' ','')
		value = value.replace('\n','')
		return key,value
	if key == '誕生日':
		key = 'birthday'
		value = value.replace(' ','')
		value = value.replace('\n','')
		return key,value
	if key == '現住所':
		key = 'address'
		value = value.replace(' ','')
		value = value.replace('\n','')
		return key,value
	if key == '出身地':
		key = 'birthplace'
		value = value.replace(' ','')
		value = value.replace('\n','')
		return key,value
	else:
		key = None
		value = None
		return key,value


#模拟登陆
def login():
	s = requests.Session()
	loginparams = {
		'email':account,
		'password':password,
		'sticky':'on',
		'post_key':'',
		'postkey':'',
		'next_url':'https://mixi.jp/home.pl'
	}
	testcode = {
		'mode':'additional_auth_post',
		'additional_auth_data_id':'',
		'year':birth_year,
		'month':birth_mon,
		'day':birth_day
	}
	try:
		#获取postkey的值
		loginhtml = s.get('https://mixi.jp',timeout = 10)
		soup_login = BeautifulSoup(loginhtml.text)
		postkey = soup_login.find(attrs = {'name':'post_key'})
		postkey_value = postkey['value']
		loginparams['post_key'] = postkey_value

		#post 登录请求
		response_login = s.post('https://mixi.jp/login.pl?from=login1', data = loginparams, headers = headers, timeout = 10)		
		#soup = BeautifulSoup(response_login.text)
		#check = soup.find('p', attrs = {'class' : 'photo'})
		#获取验证 dditional_auth_data_id 的值
		soup_test = BeautifulSoup(response_login.text)
		additional_auth_data_id = soup_test.find('input',attrs = {'name':'additional_auth_data_id'})
		#检查是否需要验证
		if additional_auth_data_id is not None:
			testcode['additional_auth_data_id'] = additional_auth_data_id['value']
			#post 验证请求
			response_test = s.post('https://mixi.jp/login.pl?from=login0', data = testcode, headers = headers, timeout = 10)
			#如果不需要验证，则返回登陆时的cookies
			print 'login success\n'
			return response_test.cookies
		else:
			print 'login success\n'
			return response_login.cookies
		'''
		html = requests.get('http://mixi.jp/show_friend.pl?id=22091183', cookies = response_test.cookies, headers = headers)
		file = open('D:\pythonSpider\mycode\data.html','w')
		file.write(html.content)
		file.close()
		'''		
	except Exception, e:
		print 'login false\n',e
		return None

if __name__ == '__main__':
	#已经下载好的用户数
	_id = 9368
	global cookies
	cookies = login()
	#使用多线程
	pool = ThreadPool(2)
	#之前已经下载好的用户数 _id
	while cookies is not None and _id < 15010:
		
		time.sleep(0)
		_id = int(_id) + 1
		start(_id)
		'''
		#此处为多线程抓取
		begin = int (_id)
		end = begin + 100
		_id = end
		pool.map(start, range(begin, end))
		'''
	
	db.close()
	pool.close()
	pool.join()

	#raw_input("Press <Enter> To Quit!")	