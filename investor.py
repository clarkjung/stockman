from order import Order
import datetime

class Investor(object):

	def __init__(self, name):
		self.name = name
		self.genkinzandaka = 10000.00
		self.current_order_list = []
		self.history_order_list = []
		self.fund_manager = None

	def hire_fund_manager(self, fund_manager):
		self.fund_manager = fund_manager

	def buy(self, stock, konyusu):
		if stock.price * konyusu > self.genkinzandaka:
			print "not enough genkinzandaka. Current genkinzandaka: " + self.genkinzandaka + ", required amount of cash: " + stock.price * number_of_stock
			return None

		new_order = Order(stock, konyusu, datetime.datetime.now(), stock.price * konyusu)
		self.current_order_list.append(new_order)
		self.genkinzandaka = self.genkinzandaka - stock.price * konyusu

	def sell(self, order):
		order.baikyaku()
		self.genkinzandaka = self.genkinzandaka + order.baikyaku_gaku
		self.current_order_list.remove(order)
		self.history_order_list.append(order)

