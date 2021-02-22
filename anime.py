#  
# Структура, которая содержит
# данные об одном аниме
# 





class Anime:
	def __init__(
		self, name=None, fields=None,
		tags=None, annotation=None, coms=[]
	):
		self.name       = name
		self.fields     = fields
		self.tags       = tags
		self.annotation = annotation
		self.coms       = coms
		return

	def rating(self):
		if self.fields['rating'] is None:
			return -1
		return self.fields['rating']

	def __lt__(lhs, rhs):
		return lhs.rating() < rhs.rating()





# END
