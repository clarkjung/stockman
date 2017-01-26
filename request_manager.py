import json
import urllib2
import csv

class RequestManager(object):

	url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22YHOO%22%20and%20startDate%20%3D%20%222009-09-11%22%20and%20endDate%20%3D%20%222010-03-10%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='

	def __init__(self):
		self.symbols = []

	def set_stock_symbols(self):
		f = open('data/nasdaq_list.csv', 'rb')
		reader = csv.reader(f)
		for row in reader:
			self.symbols.append(row[0])
		f.close()
