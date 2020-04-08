from modules import Marquee_search_transform_load,get_conn
from configparser import ConfigParser
from Sql_Transform import create_table_latest_marquee_prices,delete_recent_date_Marq,insert_recent_data_into_hist

parser = ConfigParser()
parser.read('dev.ini')

#first
Marquee_search_transform_load(parser.get('Audit','file1'),"marquee_ald_latest_data",'Aladdin')

#second 
create_table_latest_marquee_prices("marquee_ald_latest_prices",'marquee_ald_latest_data','inputs_ald_datetimes')

#third
delete_recent_date_Marq("ny_ald_hist_marquee_prices","marquee_ald_latest_data")

#fourth
insert_recent_data_into_hist("ny_ald_hist_marquee_prices","marquee_ald_latest_data")

