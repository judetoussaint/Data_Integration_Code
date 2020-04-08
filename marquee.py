import sys
import pysftp
from modules import Marquee_search_transform_load,get_conn,marquee_reprocess,marquee_backup
from configparser import ConfigParser
from modules import latest_marquee_prices,delete_recent_date_Marq,insert_recent_data_into_hist

parser = ConfigParser()
parser.read('dev.ini')

if sys.argv[1] == 'normal' and sys.argv[2] == 'aladdin':
    try:
        Marquee_search_transform_load(parser.get('Audit','file1'),"ny_marquee_ald_latest_data","Aladdin")
        latest_marquee_prices('ny_marquee_ald_latest_prices','ny_marquee_ald_latest_data','NY_Input_ALD_date_times')
        delete_recent_date_Marq("ny_ald_hist_marquee_prices","ny_marquee_ald_latest_prices")
        insert_recent_data_into_hist("ny_ald_hist_marquee_prices","ny_marquee_ald_latest_prices")
    except Exception as e:
        print(e)

elif sys.argv[1] == 'normal' and sys.argv[2] == 'frozen':
    try:
        Marquee_search_transform_load(parser.get('Audit','file2'),"ny_marquee_frz_latest_data","Frozen")
        latest_marquee_prices('ny_marquee_frz_latest_prices','ny_marquee_frz_latest_data','NY_Input_FRZ_date_times')
        delete_recent_date_Marq("ny_frz_hist_marquee_prices","ny_marquee_frz_latest_prices")
        insert_recent_data_into_hist("ny_frz_hist_marquee_prices","ny_marquee_frz_latest_prices")
    except Exception as e:
        print(e)

elif sys.argv[1] == 'normal' and sys.argv[2] == 'lionking':
    try:
        Marquee_search_transform_load(parser.get('Audit','file3'),"ny_marquee_tlk_latest_data","LionKing")
        latest_marquee_prices('ny_marquee_tlk_latest_prices','ny_marquee_tlk_latest_data','NY_Input_TLK_date_times')
        delete_recent_date_Marq("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_prices")
        insert_recent_data_into_hist("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_prices")
    except Exception as e:
        print(e)

elif sys.argv[1] == 'backup' and sys.argv[2] == 'aladdin':
    try:
        marquee_backup('ny_marquee_ald_latest_data','ny_ald_hist_marquee_prices','Aladdin')
        latest_marquee_prices('ny_marquee_ald_latest_prices','ny_marquee_ald_latest_data','NY_Input_ALD_date_times')
        delete_recent_date_Marq("ny_ald_hist_marquee_prices","ny_marquee_ald_latest_prices")
        insert_recent_data_into_hist("ny_ald_hist_marquee_prices","ny_marquee_ald_latest_prices")
    except Exception as e:
        print(e)

elif sys.argv[1] == 'backup' and sys.argv[2] == 'frozen':
    try:
        marquee_backup('ny_marquee_frz_latest_data','ny_frz_hist_marquee_prices','aladdin')
        latest_marquee_prices('ny_marquee_frz_latest_prices','ny_marquee_frz_latest_data','NY_Input_FRZ_date_times')
        delete_recent_date_Marq("ny_frz_hist_marquee_prices","ny_marquee_frz_latest_prices")
        insert_recent_data_into_hist("ny_frz_hist_marquee_prices","ny_marquee_frz_latest_prices")
    except Exception as e:
        print(e)

elif sys.argv[1] == 'backup' and sys.argv[2] == 'lionking':
    try:
        marquee_backup('ny_marquee_tlk_latest_data','ny_tlk_hist_marquee_prices','lionking')
        latest_marquee_prices('ny_marquee_tlk_latest_prices','ny_marquee_tlk_latest_data','NY_Input_TLK_date_times')
        delete_recent_date_Marq("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_prices")
        insert_recent_data_into_hist("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_prices")
    except Exception as e:
        print(e)

elif sys.argv[1] == 'reprocess' and sys.argv[2] == 'aladdin':
    try:
        marquee_reprocess(parser.get('Audit','file1'),"ny_marquee_ald_latest_data",'Aladdin','NY_ALD_marquee_reprocess')
        latest_marquee_prices('ny_marquee_ald_latest_prices','ny_marquee_ald_latest_data','NY_Input_ALD_date_times')
        delete_recent_date_Marq("ny_ald_hist_marquee_prices","ny_marquee_ald_latest_prices")
        insert_recent_data_into_hist("ny_ald_hist_marquee_prices","ny_marquee_ald_latest_prices")
    except Exception as e:
        print(e)

elif sys.argv[1] == 'reprocess' and sys.argv[2] == 'frozen':
    try:
        marquee_reprocess(parser.get('Audit','file2'),"ny_marquee_frz_latest_data",'Frozen','NY_FRZ_marquee_reprocess')
        latest_marquee_prices('ny_marquee_frz_latest_prices','ny_marquee_frz_latest_data','NY_Input_FRZ_date_times')
        delete_recent_date_Marq("ny_frz_hist_marquee_prices","ny_marquee_frz_latest_prices")
        insert_recent_data_into_hist("ny_frz_hist_marquee_prices","ny_marquee_frz_latest_prices")
    except Exception as e:
        print(e)
        
elif sys.argv[1] == 'reprocess' and sys.argv[2] == 'lionking':
    try:
        marquee_reprocess(parser.get('Audit','file2'),"ny_marquee_frz_latest_data",'Frozen','NY_FRZ_marquee_reprocess')
        latest_marquee_prices('ny_marquee_tlk_latest_prices','ny_marquee_tlk_latest_data','NY_Input_TLK_date_times')
        delete_recent_date_Marq("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_prices")
        insert_recent_data_into_hist("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_prices")
    except Exception as e:
        print(e)
       









    

