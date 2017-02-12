from investor import Investor
from fund_manager import FundManager

investor = Investor("Ariyoshi")
fund_manager = FundManager()
investor.hire_fund_manager(fund_manager)
fund_manager.set_dates()
fund_manager.run_analysis()

