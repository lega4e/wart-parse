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

	def __lt__(lhs, rhs):
		return lhs.fields['rating'] < rhs.fields['rating']





# END
