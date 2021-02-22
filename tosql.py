# 
# Модуль, который переводит аниме
# из python-представления в sql
# 

from anime import Anime





def anime2sql(anime : list [Anime] or Anime) -> str:
	'''
	Преобразовать аниме список или один класс
	'''
	if isinstance(anime, list):
		return (
			'insert into anime\n' +
			'	( name, engname, country,\n' +
			'	  year, season, target,\n' +
			'	  base, director, score,\n' +
			'	  bscore, voted, rating ) values\n' +
			'\n'.join([ one_anime_to_sql(a) for a in anime ])
	else:
		return ( "	('%s', '%s', '%s', %i, %i, '%s', '%s', '%s', %.1f, %.f, %i, %i)" %
		    ( a.name                       if a.name                       is not None else 'null',
			  a.fields['engname']          if a.fields['engname']          is not None else 'null',
			  a.fields['country']          if a.fields['country']          is not None else 'null',
			  a.fields['season']['year']   if a.fields['season']['year']   is not None else 'null',
			  a.fields['season']['season'] if a.fields['season']['season'] is not None else 'null',
			  a.fields['target']           if a.fields['target']           is not None else 'null',
			  a.fields['base']             if a.fields['base']             is not None else 'null',
			  a.fields['director']         if a.fields['director']         is not None else 'null',
			  a.fields['score']            if a.fields['score']            is not None else 'null',
			  a.fields['bscore']           if a.fields['bscore']           is not None else 'null',
			  a.fields['voted']            if a.fields['voted']            is not None else 'null',
			  a.fields['rating']           if a.fields['rating']           is not None else 'null', ))





# end
