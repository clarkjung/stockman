class HiashiNormalData(object):

	def __init__(self, date, open, close, high, low):
		self.date = date
		self.open = open
		self.close = close
		self.high = high
		self.low = low

	def print_out(self):
		print(self.date + ", open: " + self.open + ", close: " + self.close + ", high: " + self.high + ", low: " + self.low)