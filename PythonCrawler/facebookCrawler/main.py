#!/usr/bin/env python
# -*- coding:utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from cookielib import LWPCookieJar
import requests
import random
import os
import sys
import io
import time
import thread
import re

IMAGE_NUM = 0
USER_ID = 100010625445795
URL_PHOTO_ALBUM_FRONT = 'https://www.facebook.com/profile.php?id='
URL_PHOTO_ALBUM_END = '&sk=photos'
DOWNLOAD_PATH = 'E:\\ranjun\\data\\facebookData\\'

URL_LOGIN = 'https://www.facebook.com/login.php?login_attempt=1&lwv=100'
LOCAL_PATH = 'E:\\ranjun\\data\\'
COOKIES_FILE = LOCAL_PATH + 'cookies'
TIME = time.time()

#账号不同，所抓取的页面元素也不同
#10 1
#13 3

SELECT_NUM = 0
USER = [
  {
    'email' : 'xxxxxxx',
    'pass' : 'xxxxxx'
  },
  {
    'email' : 'xxxxxxxx',
    'pass' : 'xxxxxxx'
  },
  {
    'email' : 'xxxxxxxxxx',
    'pass' : 'xxxxxx'
  },
]

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
#   DO: save html for debug
#   @param:
#     page: content
#     name: file name
def save_page(page, name):
  file = open(LOCAL_PATH + name + '.html','w')
  file.write(page)
  file.close()


#function start
def start(name):
  global s
  global USER_ID
  global TIME
  check_num = 1
  if time.time() - TIME > 3600 / 2:
    TIME = time.time()
    while(login(check_num) == False):
      check_num += 1
      if check_num > 5:
        check_num = 1

  USER_ID = USER_ID - 1
  user_id = USER_ID
  print 'Download and user id =',str(user_id)
  url = URL_PHOTO_ALBUM_FRONT + str(user_id) + URL_PHOTO_ALBUM_END
  try:
    page = s.get(url = url, headers = headers, timeout = 10)
    soup = BeautifulSoup(page.content)
    divs = soup.findAll('div', attrs = {
      'class' : 'hidden_elem'
    })
    code_text = BeautifulSoup(divs[13].contents[0].contents[0])
    if len(divs) < 13:
      print u'Nonexistent user'
    else:
      code_text = BeautifulSoup(divs[13].contents[0].contents[0])	
      links = code_text.findAll('a', attrs = {
        'class' : 'uiMediaThumb _6i9 uiMediaThumbMedium'
      })
      if links is None:
        print u'No public picture'
      else:
        for link in links:
          pic_page(user_id, link['href'])
  except Exception,e:
    pass
    # print 'start error:',e


#function pic_page
#   DO:get picture's link
#   @param:
#     user_id: download user id
#     link   : get picture's links page link	
def pic_page(user_id, link):
  time.sleep(0.7)
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
    pass
    # print 'pic_page error:',e


# function download_pic
#   DO:download picture
#   @param:
#     img_url : image's download url
#     user_id : download user id
def download_pic(img_url, user_id):
  global IMAGE_NUM
  global s
  download_path = DOWNLOAD_PATH + str(user_id)
  if not os.path.exists(download_path):
    os.mkdir(download_path)
    try:
      data = s.get(img_url, timeout = 10, headers = headers).content
      IMAGE_NUM += 1
      num = IMAGE_NUM
      fileName = str(int(time.time()))  + '_' + str(num) + '.jpg'
      filePath = download_path + '\\' + fileName
      image = open(filePath, 'wb')
      image.write(data)
      image.close()
      print u'Success: ' , filePath + '\n'
    except Exception,e:
      pass
      # print "download_pic error: ",e


#function check_cookies
#   DO:check cookies weather exist
def check_cookies():
  print 'Beginning...'
  if not os.path.exists(COOKIES_FILE):
    if login(1):
      return True
    return False
  else:
    s.cookies.load()
    print 'Load cookies success'
    return True


#function login
#   DO:login and save cookies into file
def login(check):
  global SELECT_NUM
  global USER
  global s
  temp_s = requests.Session()
  if check > 5:
    SELECT_NUM += 1
    SELECT_NUM %= len(USER)
  login_params = USER[SELECT_NUM]
  print 'trying login %d time(s)' % check		
  print 'account =', login_params['email']	
  login_page = temp_s.get(URL_LOGIN)
  cookies = login_page.cookies
  try:
    login_res = temp_s.post(url = URL_LOGIN,
                           data = login_params,
                        cookies = cookies,
                        headers = headers,
                        timeout = 10)

    is_success = check_login_success(login_res.text)
    if is_success:
      s = temp_s
      SELECT_NUM += 1
      SELECT_NUM %= len(USER)
      print 'login success!'
    else:
      print 'login fail!'
    return is_success
  except Exception,e:
    print 'login error:',e
    return False


def check_login_success(html):
  pattern = re.compile(r'_mp3\s_mp3')
  m = pattern.search(html)
  if m == None:
    return False
  return True


#function crawl
#	DO:start crawl data
#	@param:
#		name : thread name
#		delay: delay time
def crawl(name,delay):
  global USER_ID
  while USER_ID > 0:
    time.sleep(delay)
    start(name)


#function main
#   DO:create thread
def main():
  global TIME
  TIMR = time.time()
  if check_cookies():
    print 'start working...'
    try:
      #you can add any threads
      delay_time = 1
      thread.start_new_thread(crawl,('thread-1', 0.3 + delay_time))
      thread.start_new_thread(crawl,('thread-2', 0.8 + delay_time))
    except Exception,e:
      print 'thread error:',e
      crawl('main',0.5)
  else:
    print 'Login fail. Please check your user and password!'
    print 'Test your account in network and try again'


if __name__ == '__main__':
  main()