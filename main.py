from request_manager import RequestManager

date1 = (2004, 2, 1)
date2 = (2004, 4, 12)

request_manager = RequestManager()
request_manager.retrieve_hiashi_normal_data('AAPL', date1, date2)
request_manager.plot_hiashi_heikinashi_data()



