import requests
import string
import os

from bs4 import BeautifulSoup

dictionary = {}
for i in string.punctuation:
	dictionary[i] = dictionary.get(i, '')
dictionary[' '] = '_'

n = int(input())
needed_type = input().replace('&', 'And')

request = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
response = requests.get(request)

resp_tree = BeautifulSoup(response.content, 'html.parser')
pages_tree = resp_tree.find_all('article')

root_folder = os.getcwd()

for i, page in enumerate(pages_tree):
	if not os.path.isdir('Page_' + str(i + 1)):
		os.mkdir('Page_' + str(i + 1))

	page = page.find('h3', {'class': 'c-card__title'})
	response = requests.get('https://www.nature.com' + page.find('a').get('href'))
	resp_tree = BeautifulSoup(response.content, 'html.parser')

	page_type = resp_tree.find('span', {'class': 'c-article-identifiers__type'})
	if page_type is None:
		page_type = resp_tree.find('li', {'class': 'c-article-identifiers__item'})
	page_type = page_type.text.title()

	if page_type != needed_type:
		continue
	if page_type == 'Publisher Correction' or page_type == 'Article' or page_type == 'Matters Arising':
		title = resp_tree.find('h1', {'class': 'c-article-title'}).text
	else:
		title = resp_tree.find('h1', {'class': 'c-article-magazine-title'}).text

	for symbol, new_symbol in dictionary.items():
		if symbol in title:
			title = title.replace(symbol, new_symbol)

	if page_type == needed_type:
		if os.path.isdir('Page_' + str(n)):
			os.chdir('Page_' + str(n))
		else:
			os.mkdir('Page_' + str(n))
	else:
		os.chdir('Page_' + str(i + 1))
	f = open(title + '.txt', 'wb')

	if page_type == 'Nature Podcast' or page_type == 'Career Column' or page_type == 'Obituary' or page_type == 'News':
		articles_tree = resp_tree.find_all('div', {'class': 'c-article-body u-clearfix'})
	elif page_type == 'Publisher Correction' or page_type == 'News Round-Up' or page_type == 'Article':
		articles_tree = resp_tree.find_all('div', {'class': 'c-article-body'})
	elif page_type == 'Matters Arising':
		articles_tree = resp_tree.find_all('div', {'class': 'c-article-section__content'})
	elif page_type == 'News And Views':
		articles_tree = resp_tree.find_all('p', {'class': 'article__teaser'})

	for article in articles_tree:
		text = article.text.encode()
		f.write(text)
	f.close()
	os.chdir(root_folder)
