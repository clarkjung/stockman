import datetime

class Order(object):

	def __init__(self, stock, hoyusu, konyu_nichiji, konyu_gaku):
		self.stock = stock
		self.hoyusu = hoyusu
		self.konyu_nichiji = konyu_nichiji
		# konyu_gaku is a total gaku
		self.konyu_gaku = konyu_gaku
		self.baikyaku_nichiji = None
		self.baikyaku_gaku = None
		self.rieki = None

	def baikyaku(self):
		self.baikyaku_nichiji = datetime.datetime.now()
		self.baikyaku_gaku = self.stock.price * self.hoyusu
		self.rieki = baikyaku_gaku - konyu_gaku