import csv
from hiashi_normal_data import HiashiNormalData
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from hiashi_normal_data import HiashiNormalData
from hiashi_heikinashi_data import HiashiHeikinashiData

class RequestManager(object):

	def __init__(self):
		self.symbols = []
		self.set_stock_symbols()
		self.hiashi_heikinashi_data_tuple_list = []

	def set_stock_symbols(self):
		f = open('data/nasdaq_list.csv', 'rb')
		reader = csv.reader(f)
		for row in reader:
			self.symbols.append(row[0])
		f.close()

	# example date format = (2004, 4, 12)
	def retrieve_hiashi_normal_data(self, symbol, from_date, to_date):
		# each quote tuple represents (date, open, close, high, low, volume)
		quotes = quotes_historical_yahoo_ohlc(symbol, from_date, to_date)

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















		