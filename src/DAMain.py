from datetime import datetime
from dataanalysis.data_analysis import DataAnalysis

da = DataAnalysis()
da.execute(update_type='daily')
if datetime.now().day == 1:
    da.execute(update_type='monthly')