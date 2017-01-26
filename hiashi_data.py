class HiashiData(object):

	def __init__(self, date, open, close, high, low):
		self.date = date
		self.open = open
		self.close = close
		self.high = high
		self.low = low

	def print(self):
		print(date, ", open: ", open, ", close: ", close, ", high: ", high, ", low: ", low)