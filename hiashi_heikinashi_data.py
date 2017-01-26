class HiashiHeikinashiData(object):

	"""
	if this is the first data, previous_hiashi_heikinashi_data 
	is replaced with previous_hiashi_normal_data

	"""
	def __init__(self, previous_hiashi_heikinashi_data, current_hiashi_normal_data, is_first_data):
		self.date = current_hiashi_normal_data.date
		self.close = (current_hiashi_normal_data.open + current_hiashi_normal_data.close + current_hiashi_normal_data.high + current_hiashi_normal_data.low)/4
		self.high = current_hiashi_normal_data.high
		self.low = current_hiashi_normal_data.low

		if is_first_data:
			self.open = (previous_hiashi_heikinashi_data.open + previous_hiashi_heikinashi_data.close + previous_hiashi_heikinashi_data.high + previous_hiashi_heikinashi_data.low)/4
		else:
			self.open = (previous_hiashi_heikinashi_data.open + previous_hiashi_heikinashi_data.close)/2
			
	def print_out(self):
		print(self.date + ", open: " + self.open + ", close: " + self.close + ", high: " + self.high + ", low: " + self.low)