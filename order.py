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

	def baikyaku(self, baikyaku_nichiji, baikyaku_gaku):
		self.baikyaku_nichiji = baikyaku_nichiji
		self.baikyaku_gaku = baikyaku_gaku
		self.rieki = baikyaku_gaku - konyu_gaku