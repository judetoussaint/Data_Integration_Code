from modules import Marquee_search_transform_load,get_conn
from configparser import ConfigParser
from modules import create_table_latest_marquee_prices,delete_recent_date_Marq,insert_recent_data_into_hist

parser = ConfigParser()
parser.read('dev.ini')

#first
Marquee_search_transform_load(parser.get('Audit','file2'),"ny_marquee_frz_latest_data","Frozen")

#second
delete_recent_date_Marq("ny_frz_hist_marquee_prices","ny_marquee_frz_latest_data")

#third
insert_recent_data_into_hist("ny_frz_hist_marquee_prices","ny_marquee_frz_latest_data")

