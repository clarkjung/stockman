import csv
import pdb
import urllib2
import pdb
from datetime import datetime
from datetime import timedelta
from hiashi_normal_data import HiashiNormalData
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
import matplotlib.dates as dt
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from hiashi_normal_data import HiashiNormalData
from hiashi_heikinashi_data import HiashiHeikinashiData
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

class FundManager(object):

	# bunseki kikan = 120 days from today
	bunseki_kikan = 180
	resistance_haba = 5

	def __init__(self):
		self.symbols = []
		self.set_stock_symbols()
		self.hiashi_heikinashi_data_tuple_list = []
		self.hiashi_heikinashi_data_list = []
		self.hiashi_normal_data_tuple_list = []
		self.hiashi_normal_data_list = []
		self.resistance_line_list = []
		self.from_date = None
		self.to_date = None

	def set_stock_symbols(self):
		f = open('data/nasdaq_list_sample.csv', 'rb')
		reader = csv.reader(f)
		for row in reader:
			self.symbols.append(row[0])
		f.close()

	def set_dates(self):
		current_date = datetime.now()
		# need to check if to_date should be today or yesterday
		self.to_date = (current_date.year, current_date.month, current_date.day)
		past_date = current_date - timedelta(days=FundManager.bunseki_kikan)
		self.from_date = (past_date.year, past_date.month, past_date.day)

	def retrieve_hiashi_normal_data(self, symbol):

		if self.from_date == None or self.to_date == None:
			print "from_date or to_date has not been set properly. "
			return None

		try:
			# each quote tuple represents (date, open, high, low, close, volume)
			quotes = quotes_historical_yahoo_ohlc(symbol, self.from_date, self.to_date)

		except urllib2.HTTPError as err:
			if err.code == 404:
				print "404 error. It probably means that there exists no such symbol. "
				return None
			else:
				print "Not 404 error. No idea why the request failed. "
				return None

		# create hiashi_normal_data from quotes
		# date, open, high, low, close
		for quote in quotes:
			hiashi_normal_data = HiashiNormalData(quote[0], quote[1], quote[2], quote[3], quote[4])
			self.hiashi_normal_data_list.append(hiashi_normal_data)

		# convert hiashi_normal_data to hiashi_heikinashi_data
		for index in range(len(self.hiashi_normal_data_list)):
			if index == 0:
				continue
			elif index == 1:
				hiashi_heikinashi_data = HiashiHeikinashiData(self.hiashi_normal_data_list[index-1], self.hiashi_normal_data_list[index], True)
				self.hiashi_heikinashi_data_list.append(hiashi_heikinashi_data)
			else:
				hiashi_heikinashi_data = HiashiHeikinashiData(self.hiashi_heikinashi_data_list[index-2], self.hiashi_normal_data_list[index], False)
				self.hiashi_heikinashi_data_list.append(hiashi_heikinashi_data)

		# convert hiashi_heikinashi_data_list to hiashi_heikinashi_data_tuple_list for plotting
		for hiashi_heikinashi_data in self.hiashi_heikinashi_data_list:
			self.hiashi_heikinashi_data_tuple_list.append(tuple([hiashi_heikinashi_data.date, hiashi_heikinashi_data.open, hiashi_heikinashi_data.high, hiashi_heikinashi_data.low, hiashi_heikinashi_data.close]))

		# convert hiashi_normal_data_list to hiashi_normal_data_tuple_list for plotting
		for hiashi_normal_data in self.hiashi_normal_data_list:
			self.hiashi_normal_data_tuple_list.append(tuple([hiashi_normal_data.date, hiashi_normal_data.open, hiashi_normal_data.high, hiashi_normal_data.low, hiashi_normal_data.close]))

		# print tuple(self.hiashi_heikinashi_data_tuple_list)

	def plot_data(self, which_data_tuple_list):

		"""
		if hiashi_heikinashi_data_tuple_list is empty, 
		that means the data was not successfully retrieved, 
		so we don't plot anything.
		"""
		if not which_data_tuple_list:
			return None

		mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
		alldays = WeekdayLocator()              # minor ticks on the days
		weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
		dayFormatter = DateFormatter('%d')      # e.g., 12

		fig, ax = plt.subplots()
		fig.subplots_adjust(bottom=0.2)
		ax.xaxis.set_major_locator(mondays)
		ax.xaxis.set_minor_locator(alldays)
		ax.xaxis.set_major_formatter(weekFormatter)
		#ax.xaxis.set_minor_formatter(dayFormatter)

		#plot_day_summary(ax, quotes, ticksize=3)
		candlestick_ohlc(ax, tuple(which_data_tuple_list), width=0.6)

		ax.xaxis_date()
		ax.autoscale_view()
		plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

		# display all resistance lines
		# for resistance_line in self.resistance_line_list:
		# 	plt.axhline(y=resistance_line, color='r', linestyle='-')

		clustered_resistance_lines = self.mean_shift(self.resistance_line_list)
		for clustered_resistance_line in clustered_resistance_lines:
			plt.axhline(y=clustered_resistance_line, color='y', linestyle='-')

		plt.show()

	def run_analysis(self, symbol = None):
		if symbol == None:
			for symbol in self.symbols:
				self.run_analysis(symbol)
		else:
			self.retrieve_hiashi_normal_data(symbol)
			self.find_all_resistance_lines()
			# do something
			#print self.resistance_line_list
			self.plot_data(self.hiashi_normal_data_tuple_list)
			self.reset_variables()

	def reset_variables(self):
		self.hiashi_heikinashi_data_tuple_list = []
		self.hiashi_heikinashi_data_list = []
		self.hiashi_normal_data_tuple_list = []
		self.hiashi_normal_data_list = []
		self.resistance_line_list = []

	def find_all_resistance_lines(self):

		# print all hiashi_normal_data_list
		for hiashi_normal_data in self.hiashi_normal_data_list:
			print("{}, {}, {}, {}, {}".format(dt.num2date(hiashi_normal_data.date), hiashi_normal_data.open, hiashi_normal_data.high, hiashi_normal_data.low, hiashi_normal_data.close))

		for index in range(len(self.hiashi_normal_data_list)):
			if index == 0 or index == len(self.hiashi_normal_data_list)-1:
				continue
			previous_high = self.hiashi_normal_data_list[index-1].high
			current_high = self.hiashi_normal_data_list[index].high
			next_high = self.hiashi_normal_data_list[index+1].high
			# print (current_high - previous_high, current_high - next_high)
			if current_high > previous_high and current_high > next_high:
				self.resistance_line_list.append(current_high)
				print("{}, {}, {}".format(previous_high, current_high, next_high))
				print("{}: {}".format(dt.num2date(self.hiashi_normal_data_list[index].date), current_high))

	def mean_shift(self, resistance_lines):
		clustered_resistance_lines = []
		print "resistance_lines"
		print resistance_lines
		X = np.array(zip(resistance_lines,np.zeros(len(resistance_lines))), dtype=np.longdouble)
		bandwidth = 0.0
		quantile_value = 0.001
		while True:
			try:
				bandwidth = estimate_bandwidth(X, quantile=quantile_value)
				while (bandwidth == 0):
					quantile_value = quantile_value + 0.001
					bandwidth = estimate_bandwidth(X, quantile=quantile_value)
				break
			except ValueError:
				quantile_value = quantile_value + 0.001

		print("{}, {}".format(quantile_value, bandwidth))

		ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
		ms.fit(X)
		labels = ms.labels_
		cluster_centers = ms.cluster_centers_
		labels_unique = np.unique(labels)
		n_clusters_ = len(labels_unique)

		print "X.toList()"
		print X.tolist()
		print len(X)

		for k in range(n_clusters_):
			# print len(X[k][0])
			print X[k][0]
			clustered_resistance_lines.append(X[k][0])

		for k in range(n_clusters_):
			my_members = labels == k
			print "cluster {0}: {1}".format(k, X[my_members, 0])
			print X[my_members, 0].tolist()
			print len(X[my_members, 0].tolist())
			cluster_resistance_value = 0
			number_of_resistance_lines = 0
			for resistance_value in X[my_members, 0].tolist():
				cluster_resistance_value += resistance_value
				number_of_resistance_lines += 1

			if number_of_resistance_lines != 0:
				cluster_resistance_value = cluster_resistance_value / number_of_resistance_lines
				clustered_resistance_lines.append(cluster_resistance_value)


		print "clustered_resistance_lines"
		print clustered_resistance_lines

		return clustered_resistance_lines