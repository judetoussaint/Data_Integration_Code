import sys
from modules import trans_file_to_load, transaction_reprocess_all
from configparser import ConfigParser
from datetime import datetime,timedelta
parser = ConfigParser()
parser.read('dev.ini')

if sys.argv[1] == 'normal' and sys.argv[2] == 'aladdin':
    try:
        trans_file_to_load('ny_trans_ald_latest_data','Disney','ny_ald_hist_transaction_data')
    except Exception as e:
        print(e)

elif sys.argv[1] == 'normal' and sys.argv[2] == 'frozen':
    try:
        trans_file_to_load('ny_trans_frz_latest_data','Frozen','ny_frz_hist_transaction_data')
    except Exception as e:
        print(e)

elif sys.argv[1] == 'normal' and sys.argv[2] == 'lionking':
    try:
        trans_file_to_load('ny_trans_tlk_latest_data','LionKing','ny_tlk_hist_transaction_data')
    except Exception as e:
        print(e)

elif sys.argv[1] == 'reprocess' and sys.argv[2] == 'aladdin':
    try:
        transaction_reprocess_all('ny_trans_ald_latest_data','Disney','NY_ALD_transaction_reprocess','ny_ald_hist_transaction_data')
    except Exception as e:
        print(e)

elif sys.argv[1] == 'reprocess' and sys.argv[2] == 'frozen':
    try:
        transaction_reprocess_all('ny_trans_frz_latest_data','Frozen','NY_FRZ_transaction_reprocess','ny_frz_hist_transaction_data')
    except Exception as e:
        print(e)

elif sys.argv[1] == 'reprocess' and sys.argv[2] == 'lionking':
    try:
        transaction_reprocess_all('ny_trans_tlk_latest_data','LionKing','NY_TLK_transaction_reprocess','ny_tlk_hist_transaction_data')
    except Exception as e:
        print(e)


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