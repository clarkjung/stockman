import csv
import pdb
import urllib2
from datetime import datetime
from datetime import timedelta
from hiashi_normal_data import HiashiNormalData
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from hiashi_normal_data import HiashiNormalData
from hiashi_heikinashi_data import HiashiHeikinashiData

class FundManager(object):

	# bunseki kikan = 120 days from today
	bunseki_kikan = 120

	def __init__(self):
		self.symbols = []
		self.set_stock_symbols()
		self.hiashi_heikinashi_data_tuple_list = []
		self.from_date = None
		self.to_date = None

	def set_stock_symbols(self):
		f = open('data/nasdaq_list.csv', 'rb')
		reader = csv.reader(f)
		for row in reader:
			self.symbols.append(row[0])
		f.close()

	def set_dates(self):
		current_date = datetime.now()
		# need to check if to_date should be today or yesterday
		self.to_date = (current_date.year, current_date.month, current_date.day)
		past_date = current_date - timedelta(days=bunseki_kikan)
		self.from_date = (past_date.year, past_date.month, past_date.day)

	def retrieve_hiashi_normal_data(self, symbol):

		if self.from_date == None or self.to_date == None:
			print "from_date or to_date has not been set properly. "
			return None

		try:
			# each quote tuple represents (date, open, close, high, low, volume)
			quotes = quotes_historical_yahoo_ohlc(symbol, self.from_date, self.to_date)

		except urllib2.HTTPError as err:
			if err.code == 404:
				print "404 error. It probably means that there exists no such symbol. "
				return None
			else:
				print "Not 404 error. No idea why the request failed. "
				return None

		# create hiashi_normal_data from quotes
		hiashi_normal_data_list = []
		hiashi_heikinashi_data_list = []
		for quote in quotes:
			hiashi_normal_data = HiashiNormalData(quote[0], quote[1], quote[2], quote[3], quote[4])
			hiashi_normal_data_list.append(hiashi_normal_data)

		# convert hiashi_normal_data to hiashi_heikinashi_data
		for index in range(len(hiashi_normal_data_list)):
			if index == 0:
				continue
			elif index == 1:
				hiashi_heikinashi_data = HiashiHeikinashiData(hiashi_normal_data_list[index-1], hiashi_normal_data_list[index], True)
				hiashi_heikinashi_data_list.append(hiashi_heikinashi_data)
			else:
				hiashi_heikinashi_data = HiashiHeikinashiData(hiashi_heikinashi_data_list[index-2], hiashi_normal_data_list[index], False)
				hiashi_heikinashi_data_list.append(hiashi_heikinashi_data)

		# convert hiashi_heikinashi_data_list to hiashi_heikinashi_data_tuple_list for plotting
		for hiashi_heikinashi_data in hiashi_heikinashi_data_list:
			self.hiashi_heikinashi_data_tuple_list.append(tuple([hiashi_heikinashi_data.date, hiashi_heikinashi_data.open, hiashi_heikinashi_data.close, hiashi_heikinashi_data.high, hiashi_heikinashi_data.low]))

		print tuple(self.hiashi_heikinashi_data_tuple_list)

	def plot_hiashi_heikinashi_data(self):

		"""
		if hiashi_heikinashi_data_tuple_list is empty, 
		that means the data was not successfully retrieved, 
		so we don't plot anything.
		"""
		if not self.hiashi_heikinashi_data_tuple_list:
			return None

		mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
		alldays = DayLocator()              # minor ticks on the days
		weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
		dayFormatter = DateFormatter('%d')      # e.g., 12

		fig, ax = plt.subplots()
		fig.subplots_adjust(bottom=0.2)
		ax.xaxis.set_major_locator(mondays)
		ax.xaxis.set_minor_locator(alldays)
		ax.xaxis.set_major_formatter(weekFormatter)
		#ax.xaxis.set_minor_formatter(dayFormatter)

		#plot_day_summary(ax, quotes, ticksize=3)
		candlestick_ohlc(ax, tuple(self.hiashi_heikinashi_data_tuple_list), width=0.6)

		ax.xaxis_date()
		ax.autoscale_view()
		plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

		plt.show()


















	

	def run_analysis(self, symbol = None):
		if symbol == None:
			for symbol in self.symbols:
				self.run_analysis(symbol)
		else:
			# do something
			self.reset_hiashi_heikinashi_data_tuple_list()

	def reset_hiashi_heikinashi_data_tuple_list()
		self.hiashi_heikinashi_data_tuple_list = []

