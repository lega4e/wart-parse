#
# Данный модуль отвечает за парсинг
# рейтинга аниме для получения списка
# словарей следующего формата:
# {
#    rating : int,   # 1, 2, 3, ..., 4208,
#    href   : str,   # 'http://www.world-art.ru/animation/animation.php?id=N'
#    score  : float, # 9.1875 (Расчётный балл по Байесу)
# }
#

import re
import requests as req
from bs4 import BeautifulSoup





# main
def parse_rating() -> [ dict ]:
	'''
	Парсит весь рейтинг
	'''
	url_template = 'http://www.world-art.ru/animation/rating_top.php?limit_1=%i'
	result = []

	for i in range(0, 4300, 100):
		url     = url_template % i
		text    = req.get(url).text
		soup    = BeautifulSoup(text, 'lxml')
		result += parse_rating_page(soup)

	return result




def parse_rating_page(soup) -> [ dict ]:
	'''
	Парсит отдельную страницу рейтинга
	'''
	anime_list = []

	lines = (
		soup.body.center.find_all('table')[6].
		tr.contents[2].
		center.table.td.find_all('table')[1].
		find_all('tr')[1:]
	)

	for line in lines:
		one = {}
		one['rating'] = int(line.b.text)
		one['href'] = line.a['href']
		one['score'] = float(line.contents[2].text)
		anime_list.append(one)

	return anime_list





def print_rating(rating):
	'''
	Выводит весь рейтинг
	'''
	for one in rating:
		print(one)
	return





# end
