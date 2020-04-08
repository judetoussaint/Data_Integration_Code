import sys
import pysftp
from modules import Marquee_search_transform_load,get_conn,marquee_reprocess,marquee_backup, latest_marquee_prices
from configparser import ConfigParser
from modules import delete_recent_date_Marq,insert_recent_data_into_hist

parser = ConfigParser()
parser.read('dev.ini')

# marquee_reprocess(parser.get('Audit','file1'),"marquee_ald_latest_data","Aladdin",'NY_ALD_marquee_reprocess')

# first
Marquee_search_transform_load('04_07_2020_TLKAUDIT.TXT',"ny_marquee_tlk_latest_data","LionKing")
latest_marquee_prices('ny_marquee_tlk_latest_prices','ny_marquee_tlk_latest_data','NY_Input_TLK_date_times')
delete_recent_date_Marq("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_prices")
insert_recent_data_into_hist("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_prices")




#'03-17-2020_ALADDINAUDIT.TXT'
# third
# insert_recent_data_into_hist("ny_ald_hist_marquee_prices","ny_marquee_ald_latest_data")

# create_table_latest_marquee_prices("marquee_ald_latest_prices",'marquee_ald_latest_data','inputs_ald_datetimes')





# if len(sys.argv) == 1:

#     #first
#     Marquee_search_transform_load('marquee_ald_latest_data','ny_ald_hist_marquee_prices','Aladdin')
#     #second
#     create_table_latest_marquee_prices("marquee_ald_latest_prices",'marquee_ald_latest_data','inputs_ald_datetimes')
#     #third
#     delete_recent_date_Marq("ny_ald_hist_marquee_prices","marquee_ald_latest_data")
#     #Fourth
#     insert_recent_data_into_hist("ny_ald_hist_marquee_prices","marquee_ald_latest_data")

# elif sys.argv[1] == 'backup':

#     #first
#     marquee_backup('marquee_ald_latest_data','ny_ald_hist_marquee_prices','Aladdin')
#     #second
#     create_table_latest_marquee_prices("marquee_ald_latest_prices",'marquee_ald_latest_data','inputs_ald_datetimes')
#     #third
#     delete_recent_date_Marq("ny_ald_hist_marquee_prices","marquee_ald_latest_data")
#     #fourth
#     insert_recent_data_into_hist("ny_ald_hist_marquee_prices","marquee_ald_latest_data")

# elif sys.argv[1] == 'reprocess':
#     #first
#     marquee_reprocess(parser.get('Audit','file1'),"marquee_ald_latest_data",'Aladdin','NY_ALD_marquee_reprocess')
#     #second
#     create_table_latest_marquee_prices("marquee_ald_latest_prices",'marquee_ald_latest_data','inputs_ald_datetimes')
#     #third
#     delete_recent_date_Marq("ny_ald_hist_marquee_prices","marquee_ald_latest_data")
#     #fourth
#     insert_recent_data_into_hist("ny_ald_hist_marquee_prices","marquee_ald_latest_data")






