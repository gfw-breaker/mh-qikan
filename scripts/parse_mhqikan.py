#!/usr/bin/python
# coding: utf-8

import sys
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

channel = sys.argv[1]
channel_url = sys.argv[2]

base_url = 'http://qikan.minghui.org/'
index_page = '|||||\n|---|---|---|---|\n'

def get_content(cover_url):
	content = ''
	prefix = '-'.join(cover_url.split('-')[0:-1])
	if prefix == '':
		return False

	if img_exist(prefix + '-online1.jpg'):
		img_type = '.jpg'
	elif img_exist(prefix + '-online1.png'):
		img_type = '.png' 
	else:
		return False

	for i in range(1,100):
		suffix = '-online' + str(i) + img_type
		png_url = prefix + suffix
		if img_exist(png_url):
			content += '<img src="' + png_url + '"/> \n\n'
		else:
			break
	return content


def img_exist(png_url):
	response = requests.head(png_url)
	#print response.status_code
	if response.status_code == 200:
		return True	
	else:
		return False


def write_page(name, path, title, link, content):
	body = '### ' + title + '\n\n---\n\n' + content
	body += '\n\n---\n\n#### [首页](../../../..) &nbsp;|&nbsp; '
	body += '[禁闻聚合](https://github.com/gfw-breaker/banned-news) &nbsp;|&nbsp; '
	body += '[手把手翻墙教程](https://github.com/gfw-breaker/guides) '
	fh = open(path, 'w')
	fh.write(body)
	fh.close()


def short_title(title):
	return title.split(')')[1].split('）')[0].split('，')[0] + '）'


index_text = requests.get(channel_url).text.encode('utf-8')
index_html = BeautifulSoup(index_text, 'html.parser')
articles = index_html.find('div', attrs = {'class':'qikan_listing0'}).find_all('a')
for idx in range(len(articles)):
	article = articles[idx]
	a_url = article.get('href').encode('utf-8')
	a_img  = article.find('img')
	if a_img is None:
		continue
	a_title = a_img.get('alt').encode('utf-8')
	a_cover = base_url + a_img.get('src').encode('utf-8')
	print a_title  #, a_cover
	name = a_url.split('=')[-1] + '.md'
	file_path = '../pages/' + channel + '/' + name 
	#print name, file_path

	if not os.path.exists(file_path):
		print file_path
		content = get_content(a_cover)
		if not content:
			continue
		write_page(name, file_path, a_title, a_url, content)
	index_page += '|[<img width="200px" src="' + a_cover + '" ><br/><b>' \
			+ short_title(a_title) + '</b><br/><br/>](' + file_path + ')'
	if idx % 4 == 3:
		index_page += '|\n' 


index_file = open('../indexes/' + channel + '.md', 'w')
index_file.write(index_page)
index_file.close()



