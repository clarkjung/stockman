class HiashiNormalData(object):

	def __init__(self, date, open, high, low, close):
		self.date = date
		self.open = open
		self.high = high
		self.low = low
		self.close = close

	def print_out(self):
		print(self.date + ", open: " + self.open + ", close: " + self.close + ", high: " + self.high + ", low: " + self.low)