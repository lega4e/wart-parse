#!/usr/bin/python3
import datetime as dt
import pickle
import requests as req
import time
import threading as thd

from bs4 import BeautifulSoup

import tosql
import parse_anime_page   as pa
import parse_anime_rating as pr

from anime import Anime





# objects
rating      = [ { 'href' : 'http://www.world-art.ru/animation/animation.php?id=3' } ]
rating_lock = thd.Lock()
rating_i    = 0

anime      = []
anime_lock = thd.Lock()

tags      = dict()
tags_lock = thd.Lock()

total_time = None

max_tag_len = 0
max_ann_len = 0
max_com_len = 0

stdout_lock = thd.Lock()





# types
class Parser (thd.Thread):
	def __init__(self, id):
		thd.Thread.__init__(self)
		self.id = id
		return

	def run(self):
		global rating, rating_i, rating_lock
		global anime, anime_lock

		while True:
			try:
				# ger href
				with rating_lock:
					if rating_i >= len(rating):
						return
					rat = rating[rating_i]
					rating_i += 1

				# try parse
				while True:
					text = req.get(rat['href']).text
					soup = BeautifulSoup(text, 'lxml')
					a = parse_anime(soup)
					if a is not None:
						a.fields['bscore'] = ret['score']
						break
					print('inc', rat['href'], '(%i)' % self.id)
					time.sleep(0.2)

				# add to anime list
				with anime_lock:
					anime.append(a)
					al = len(anime)

				# add tags to tag list
				with tags_lock:
					for tag in a.tags:
						tags[tag] = a.tags[tag]['desc']

				# print log
				with stdout_lock:
					print(
						'anime #%i done (%.2f%%)' %
						(a.fields['rating'], 100 * al / len(rating)),
						flush=True
					)
			except:
				global th
				print('bad', url)





# rating functions
def parse_one_page(url):
	text = req.get(url).text
	soup = BeautifulSoup(text, 'lxml')
	anime = pa.parse_anime(soup)
	pa.print_anime(anime)

def parse_and_write_rating():
	global rating
	rating = pr.parse_rating()
	with open('rating.bin', 'wb') as file:
		pickle.dump(l, file)

def read_rating():
	global rating
	with open('rating.bin', 'rb') as file:
		rating = pickle.load(file)



# anime functions
def parse_all_anime():
	global rating, anime, total_time
	start_time = dt.datetime.now()

	thread_count = 8
	#  rating = rating[0:100]
	ths = []

	for i in range(thread_count):
		ths.append(Parser(i))
		ths[-1].start()

	for th in ths:
		th.join()

	anime.sort()
	end_time = dt.datetime.now()
	total_time = (end_time - start_time).total_seconds()

def write_all_anime():
	with open('anime.bin', 'wb') as file:
		pickle.dump((anime, tags, total_time), file)

def read_all_anime():
	global anime, tags, total_time
	with open('anime.bin', 'rb') as file:
		anime, tags, total_time = pickle.load(file)



# print functions
def print_all_anime():
	for a in anime:
		pa.print_anime(a)
		print('\n'*10)

def print_tags():
	for tag in tags:
		print(tag, end=' — ')
		print(tags[tag], end='\n\n')

def print_common():
	print('Total time:    ', total_time)
	print('Max len of tag:', max_tag_len)
	print('Max len of ann:', max_ann_len)
	print('Max len of com:', max_com_len)

def calculate_states():
	global max_tag_len
	global max_ann_len
	global max_com_len

	max_tag_len = 0
	max_ann_len = 0
	max_com_len = 0

	for tag in tags:
		max_tag_len = max(max_tag_len, len(tags[tag]))

	for a in anime:
		if a.annotation is not None:
			max_ann_len = max(max_ann_len, len(a.annotation))
		for com in a.coms:
			max_com_len = max(max_com_len, len(com))





# main
#  read_all_anime()


#  with open('anime.mysql', 'w') as file:
	#  file.write(tosql.anime_to_sql(anime))

read_rating()
for r in rating[:3]:
	print(r)

#  if len(anime) != len(rating):
	#  raise Exception("Error!!!!")

#  for a in anime:
	#  a.fields['bscore'] = rating[a.fields['rating']-1]['score']

#  for a in anime[4200:]:
	#  print_anime(a)
	#  print('\n'*5)

#  parse_all_anime()
#  write_all_anime()

#  time.sleep(5)

#  calculate_states()
#  print_all_anime()
#  print_tags()
#  print_common()





# END
