# 
# Модуль, который переводит аниме
# из python-представления в sql
# 

import re

from anime import Anime





def anime2sql(anime : [ Anime ] or Anime) -> str:
	'''
	Преобразовать аниме список или один класс
	'''
	if isinstance(anime, list):
		if len(anime) == 0:
			return ''
		return (
			'insert into anime_full (\n'          +
			'	name,   engname,\n'          +
			'	atype,  duration, epsc,\n'   +
			'	year,   season,   target,\n' +
			'	base,   director, score,\n'  +
			'	bscore, voted,    rating,\n' +
			'	annotation\n'                +
			#  '	com1,   com2,     com3\n'    +
			') values\n'                     +
			',\n'.join( [ anime2sql(a) for a in anime ] ) + ';\n'
		)
	return (
		( "	(\n" +
		  "		%s, %s,\n"     + # name,   engname
		  "		%s, %s, %s,\n" + # atype,  duration, epsc,
		  "		%s, %s, %s,\n" + # year,   season,   target,
		  "		%s, %s, %s,\n" + # base    director, score
		  "		%s, %s, %s,\n" + # bscore, voted,    rating
		  "		%s\n"          + # annotation
		  #  "		%s, %s, %s\n"  + # com1, com2, com3
		  "	)" ) % 
		( extract( anime.name                       ),
		  extract( anime.fields['engname']          ),

		  extract( anime.fields['type']['type']     ),
		  extract( anime.fields['type']['duration'] ),
		  extract( anime.fields['type']['epsc']     ),

		  extract( anime.fields['season']['year']   ),
		  extract( anime.fields['season']['season'] ),
		  extract( anime.fields['target']           ),

		  extract( anime.fields['base']             ),
		  extract( anime.fields['director']         ),
		  extract( anime.fields['score']            ),

		  extract( anime.fields['bscore']           ),
		  extract( anime.fields['voted']            ),
		  extract( anime.fields['rating']           ),

		  extract( anime.annotation                 )
		  #  extract( anime.coms[0]                    ),
		  #  extract( anime.coms[1]                    ),
		  #  extract( anime.coms[2]                    )
		)
	)


def genre2sql(anime : [ Anime ] or Anime) -> str:
	'''
	Записать жанры аниме из списка аниме или из одного
	'''
	if isinstance(anime, list):
		if len(anime) == 0:
			return ''
		return (
			'insert into genre ( genre, anime_rating ) values\n' +
			',\n'.join( filter(
				lambda s: len(s) != 0,
				[ genre2sql(a) for a in anime ]
			) ) + ';\n'
		)
	if anime.fields['genre'] is None:
		return ''
	return ',\n'.join( [
		'	("%s", %i)' % (genre, anime.fields['rating'])
		for genre in anime.fields['genre']
	] )

def tags2sql(tags : dict) -> str:
	if len(tags) == 0:
		return ''
	return (
		'insert into tagdesc (tag, description) values\n' +
		',\n'.join( [
			'	(%s, %s)' % (extract(tag), extract(tags[tag]))
			for tag in tags
		] ) + ';\n'
	)

def animetags2sql(anime : [ Anime ] or Anime) -> str:
	if isinstance(anime, list):
		if len(anime) == 0:
			return ''
		return (
			'insert into tag (tag, score, anime_rating) values\n' +
			',\n'.join( filter(
				lambda s: len(s) != 0,
				[ animetags2sql(a) for a in anime ] 
			) ) + ';\n'
		)
	return ',\n'.join( [
		'	(%s, %s, %s)' % (
			extract(tag),
			extract(anime.tags[tag]['score']),
			extract(anime.fields['rating'])
		)
		for tag in anime.tags
	] )




def extract(field) -> str:
	if field is None:
		return 'null'
	if isinstance(field, str):
		return '"' + re.sub(r'"', r'\"', ('%s' % field)) + '"'
	return str(field)





# end
