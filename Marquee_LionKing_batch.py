from modules import Marquee_search_transform_load,get_conn
from configparser import ConfigParser
from Sql_Transform import create_table_latest_marquee_prices,delete_recent_date_Marq,insert_recent_data_into_hist

parser = ConfigParser()
parser.read('dev.ini')

#first
Marquee_search_transform_load(parser.get('Audit','file3'),"ny_marquee_tlk_latest_data",'LionKing')

#second
delete_recent_date_Marq("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_data")

#third
insert_recent_data_into_hist("ny_tlk_hist_marquee_prices","ny_marquee_tlk_latest_data")


# create_table_latest_marquee_prices("marquee_tlk_latest_prices",'marquee_tlk_latest_data','inputs_tlk_datetimes')


