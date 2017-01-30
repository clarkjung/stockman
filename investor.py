class Investor(object):

	def __init__(self, name, genkinzandaka):
		self.name = name
		self.genkinzandaka = 10000.00
		self.stock_list = []

	def buy(self, stock, number_of_stock):
		if stock.price * number_of_stock > self.genkinzandaka:
			print "not enough genkinzandaka. Current genkinzandaka: " + self.genkinzandaka + ", required amount of cash: " + stock.price * number_of_stock
			return None

		self.genkinzandaka = self.genkinzandaka - stock.price * number_of_stock
		
