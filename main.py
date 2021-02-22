#!/usr/bin/python3
import datetime as dt
import os
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
rating      = [
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=1' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=8026' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=2763' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=3996' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=6681' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=6998' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=7' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=8' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=9' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=10' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=11' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=12' },
	#  { 'score' : 0, 'href' : 'http://www.world-art.ru/animation/animation.php?id=13' }
]
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

start_time = None
end_time = None

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
					try:
						text = req.get(rat['href']).text
						soup = BeautifulSoup(text, 'lxml')
						a = pa.parse_anime(soup, write_image=False)
						if a is not None:
							a.fields['bscore'] = rat['score']
							break
					except:
						pass
					time.sleep(0.2)

				# add to anime list
				with anime_lock:
					anime.append(a)
					al = len(anime)

				# add tags to tag list
				with tags_lock:
					for tag in a.tags:
						tags[tag] = a.tags[tag]['desc']

				# time
				cur_time = dt.datetime.now()
				delta = cur_time - start_time
				t = delta.total_seconds() * ( len(rating) / al - 1 )

				# print log
				with stdout_lock:
					print(
						'anime #%04i done, remain %2.2fs (%.2f%%)' %
						(a.fields['rating'], t, 100 * al / len(rating)),
						flush=True
					)
			except Exception as e:
				print('bad', rat['href'], flush=True)
				print(e)





# rating functions
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
	global start_time, end_time
	start_time = dt.datetime.now()

	thread_count = 32
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

def anime2sql():
	global anime
	with open('anime.mysql', 'w') as file:
		file.write(tosql.anime2sql(anime))
		file.write('\n\n')
		file.write(tosql.genre2sql(anime))
		file.write('\n\n')
		file.write(tosql.tags2sql(tags))
		file.write('\n\n')
		file.write(tosql.animetags2sql(anime))
	return



# print functions
def print_all_anime(style='short'):
	for a in anime:
		pa.print_anime(a, style=style)
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
			if com is not None:
				max_com_len = max(max_com_len, len(com))





# main
try: os.makedirs('images')
except: pass

#  read_rating()
#  parse_all_anime()
#  write_all_anime()
read_all_anime()
anime2sql()
calculate_states()
print_common()





# end
