from investor import Investor
from fund_manager import FundManager

investor = Investor("Ariyoshi")
fund_manager = FundManager()
investor.hire_fund_manager(fund_manager)

date1 = (2004, 2, 1)
date2 = (2004, 4, 12)

fund_manager.retrieve_hiashi_normal_data('PIH', date1, date2)
fund_manager.plot_hiashi_heikinashi_data()



