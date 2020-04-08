from modules import trans_file_to_load
from configparser import ConfigParser
from datetime import datetime,timedelta
parser = ConfigParser()
parser.read('dev.ini')

# print(datetime.now())
# print("LionKing_{:%Y%m%d}".format(datetime.now()-timedelta(1)))

trans_file_to_load('ny_trans_ald_latest_data','Disney','ny_ald_hist_transaction_data')

# filename = parser.get('Transaction','file1')+"{}{:%Y%m%d}{}".format("_",datetime.now()-timedelta(1),'.txt')
# print(filename)
# tablename = 'trans_ald_latest_data'
# print(tablename)

# #first step
# transaction_search_load(filename,tablename)

# #second step
# delete_recent_date_Trans("ny_ald_hist_transaction_data","trans_ald_latest_data")

# #third step
# insert_recent_data_into_hist("ny_ald_hist_transaction_data","trans_ald_latest_data")