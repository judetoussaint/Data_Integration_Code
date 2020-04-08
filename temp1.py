
from sqlalchemy import create_engine,Integer, String,Time, Float, DateTime, Date, TIMESTAMP
import pysftp
import win32com.client as win32
import time
import pandas as pd
import re
from datetime import datetime, timedelta, date
import send2trash
from modules import transform_raw, get_conn,process_indicator, alert_body,alert_subject, alert_emails,delete_recent_date_Trans
from modules import Inputs_search_load_alerts,list_files_on_FTP,process_control_start_end_date
from modules import ActorsFund_search_transform_load,Marquee_search_file_date
from configparser import ConfigParser
from Sql_Transform import create_table_latest_marquee_prices,insert_recent_data_into_hist
from Modules_manual_Inputs import Inputs_search_load_week_filter


myHostname = "filetransfer.disney.com"
myUsername = 'dtp_clients'
myPassword = 'dtp*890'

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'jude.toussaint@disney.com'
mail.Subject = 'Message subject'
mail.Body = 'Jude, the file time is not right'
#mail.CC = "more email addresses here"
#mail.BCC = "more email addresses here"


mail1 = outlook.CreateItem(0)
mail1.To = 'jude.toussaint@disney.com'
mail1.Subject = 'Dont panic but'
mail1.Body = 'The file time is still not right'

parser = ConfigParser()
parser.read('dev.ini')



# Inputs_search_load_alerts('email_role_list.csv','email_role_list')
 
# email_role_list
# alert_list
# role_alert_list

# lists = list_files_on_FTP()
# for file in lists:
# 	if 'Frozen' in file:
# 		print(file)
 

# Inputs_search_load_manuals('ALD','NY_ALD_comp_week_filter.csv','NY_ALD_comp_week_filter')

# get_date = process_control_date('NY_FRZ_transaction_purge')
# end_date = (datetime.strptime(get_date[1], '%Y-%m-%d'))
# start_date = (datetime.strptime(get_date[0], '%Y-%m-%d'))
# print(get_date)
# print(start_date)
# print(end_date)

from datetime import date, timedelta

#'NY_FRZ_transaction_purge'

def process_control_in_between_dates(process_name):
	"""This function is to get the dates in between start_date and end end_dates from process control table"""

	get_date = process_control_start_end_date(process_name)

	sdate = (datetime.strptime(get_date[0], '%Y-%m-%d'))   # start date
	edate = (datetime.strptime(get_date[1], '%Y-%m-%d'))   # end date

	delta = edate - sdate       # as timedelta

	list_days = []
	for i in range(delta.days + 1):
		day = '{0}'.format(sdate + timedelta(days=i))
		list_days.append(day)
		tuple_list_days = tuple(list_days)
	return(tuple_list_days)
	
# print(process_control_in_between_dates('NY_FRZ_transaction_purge'))

def purge_bad_data(hist_tablename,process_name):
	"""This function is to purge/delete all the dates that are needed to be purged"""
	engine = get_conn()
	engine.execute("""Delete from raw.{0} where transaction_date in {1}""".format(hist_tablename,process_control_in_between_dates(process_name)))



# purge_bad_data('ny_frz_hist_transaction_data','NY_FRZ_transaction_purge')



def search_last_modified_date(filename): #Hong call this file_date

	with pysftp.Connection(host=parser.get('FTP', 'myHostname'), username=parser.get('FTP', 'myUsername'),
		password=parser.get('FTP', 'myPassword'), port=parser.getint('FTP', 'myPort')) as sftp:
		sftp.cwd('/.')
		remotefilepath = '/'+filename
		localfilepath = './'+filename
		sftp.get(remotefilepath, localfilepath)
		attr = sftp.lstat(remotefilepath)
		attr_string = '{}'.format(attr)
		month = attr_string[44:49].strip()
		day = attr_string[41:44].strip()
		now = datetime.now()
		year = '{0}'.format(now.year)
		date = year +'-' + month + '-' + day

	return (date)

# a = Marquee_search_file_date_T('Frozen_20200328.txt')
# print(a)
# print(type(a))


# b ='{}'.format(a)
# c = b[41:49]
# print(b)
# print(type(b))
# print(c)
#'NY_ALD_transaction_reprocess'


def purge_bad_data(hist_tablename,process_name):
	"""This function is to purge/delete all the dates that are needed to be purged"""
	engine = get_conn()
	engine.execute("""Delete from raw.{0} where transaction_date in {1}""".format(hist_tablename,process_control_in_between_dates(process_name)))


def transaction_reprocess_all(table_name,show_name,process_name, hist_tablename):#Requirement 6.0
	"""This function reprocess all the transaction files given that  process_indicator='Y' and
	today's date is in between the two process_dates"""
	get_date = process_control_start_end_date(process_name)
	end_date = (datetime.strptime(get_date[1], '%Y-%m-%d'))
	# start_date = (datetime.strptime(get_date[0], '%Y-%m-%d'))
	# start_date < datetime.now() < end_date
	engine = get_conn()
	engine.execute("""Delete from raw.{0} where transaction_date in {1}""".format(hist_tablename,process_control_in_between_dates(process_name)))


	if (process_indicator(process_name)== 'Y') and (end_date <= datetime.now()):
		file_list = transaction_reprocess_list(show_name,process_name)
		for file in file_list:
			transaction_reprocess_search_load(file, table_name,show_name)

			#second step
			delete_recent_date_Trans(hist_tablename,table_name)#Maybe I can add those tables as arguments in the table

			#third step
			insert_recent_data_into_hist(hist_tablename,table_name)
	engine.execute("""update control.process_control 
					set process_indicator = 'N'
					where process_name = '{}'""".format(process_name)
					)




def transaction_reprocess_list(show_name,process_name):
	"""This functions creates the list of files that needs to be reprocessed"""
	a = process_control_in_between_dates(process_name)
# print(a)
	show_list = []
	for i in range(len(a)):
		show_list.append(show_name +'_' + a[i].split()[0].replace('-','')+'.txt')

	return(show_list)


# a = transaction_reprocess_list('Disney','NY_ALD_transaction_reprocess')
# print(a)



def transaction_reprocess_search_load(filename, table_name,show_name):
	"""This function is to reprocess a transaction file. Major difference to transaction_search_load
	is the status='Reprocess' and the email that's difference"""

	with pysftp.Connection(host=parser.get('FTP', 'myHostname'), username=parser.get('FTP', 'myUsername'),
		password=parser.get('FTP', 'myPassword'), port=parser.getint('FTP', 'myPort')) as sftp:
		sftp.cwd('/.')
		list_dir = sftp.listdir()
		# date = '{:%d-%b-%y}'.format(datetime.now()).upper()
		date = '{:%d-%b-%y}'.format(datetime.now()).upper()
		if filename in list_dir:
			print("It's there")  # Or download to S3
			remotefilepath = '/'+filename
			localfilepath = './'+filename
			sftp.get(remotefilepath, localfilepath)
			# Transaction_read_load()
			df = pd.read_csv(filename,sep='\t')
			if len(df) == 0:
				outlook = win32.Dispatch('outlook.application')
				mail = outlook.CreateItem(0)
				mail.To = "{}".format(alert_emails('14'))
				mail.Subject = "{}".format(alert_subject('14'))
				formatted_body = alert_body('14')
				mail.Body = "{}".format(formatted_body.format(show=show_name,file_name =filename, file_date=date))
				mail.Send()
				print('File is empty')
				#send an email that file is empty
			else:		
				# df = pd.read_csv(filename,sep='\t')	
				df['run_date'] = '{:%d-%b-%y}'.format(datetime.now()).upper()
				df['status'] = 'Reprocess'
				df.columns =['event_code','xnum','section','from_row','to_row','from_seat','to_seat',
				'tickets','transaction_date','transaction_time','from_status','to_status','qualifiers','account','transaction_value',
				'opcode','price_level','service_charge','facility_charge','run_date','status']	
				date = df['transaction_date'][0]	
				# dialect+driver://username:password@host:port/database
				engine = get_conn()
				df.to_sql(table_name,if_exists = 'replace', con=engine, chunksize=1000, schema='raw',index=False, 
					dtype={"event_code": String(),'xnum':Float(),'section':String(), 'from_row':String(),'to_row':String(),'from_seat':Integer(),'to_seat':Integer(),
					'tickets':Integer(),'transaction_date':Date(),'transaction_time':String(),'from_status':String(), 'to_status':String(),
					'qualifiers':String(),'account':String(),'transaction_value':Integer(),'opcode':String(), 'price_level':Integer(),
					'service_charge':Integer(), 'facility_charge':Integer(),'run_date':Date(),'status':String()})
					
				#send an email
				print('It is there. I will send first email')
				outlook = win32.Dispatch('outlook.application')
				mail = outlook.CreateItem(0)
				mail.To = "{}".format(alert_emails('11'))
				mail.Subject = "{}".format(alert_subject('11'))
				formatted_body = alert_body('11')
				mail.Body = "{}".format(formatted_body.format(show=show_name, date=date))#We might need to change this date
				mail.Send()


		else:
			print("It is not there. I will send email")#send an email
		
# a = process_indicator('NY_ALD_transaction_reprocess')
# print(a)

# a = alert_body('14')
# print(a)



# transaction_reprocess_all(table_name,show_name,process_name):

# transaction_reprocess_search_load('Frozen_20200331.txt', "ny_trans_frz_latest_data",'Frozen')


# transaction_reprocess_all('ny_trans_ald_latest_data','Disney','NY_ALD_transaction_reprocess','ny_ald_hist_transaction_data')

# filename = 'TLKACTORSFUND.TXT'
# table_name = 'ny_actfnd_tlk_latest_data'
# show_name = 'LionKing'

# filename = 'FRZACTORSFUND.TXT'
# table_name = 'ny_actfnd_frz_latest_data'
# show_name = 'Frozen'

# filename = 'ALADDINACTORSFUND.TXT'
# table_name = 'ny_actfnd_ald_latest_data'
# show_name = 'Aladdin'

# ActorsFund_search_transform_load('ALADDINACTORSFUND.TXT', 'ny_actfnd_ald_latest_data', 'Aladdin','NY_ALD_actors_fund')
# ActorsFund_search_transform_load('FRZACTORSFUND.TXT', 'ny_actfnd_frz_latest_data', 'Frozen','NY_FRZ_actors_fund')
# ActorsFund_search_transform_load('TLKACTORSFUND.TXT', 'ny_actfnd_tlk_latest_data', 'LionKing','NY_TLK_actors_fund')

# a = Marquee_search_file_date("03_02_2020_FRZAUDIT.TXT")
# print(a)
# print('2-MAR-20'.lower())


# b = (datetime.strptime('2-MAR-20'.lower(), '%d-%b-%y'))
# print(b)
# # print(type(b))
# # print(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
# print(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))

from Modules_manual_Inputs import Inputs_search_load_date_times, Inputs_search_load_DCP_info,Inputs_search_load_dynm_info
from Modules_manual_Inputs import Inputs_search_load_rate_info, Inputs_search_load_opt_const,Inputs_search_load_diff_const
from Modules_manual_Inputs import Inputs_search_load_grid_const,Inputs_search_load_level_info,Inputs_search_load_maps_past
from Modules_manual_Inputs import Inputs_search_load_maps_raw,Inputs_search_load_tier_info,Inputs_search_load_qualifier_info
from Modules_manual_Inputs import Inputs_search_load_perf_list,Inputs_search_load_id_info,Inputs_search_load_id_maps
from Modules_manual_Inputs import Inputs_search_load_nums_maps,Inputs_search_load_row_maps,Inputs_search_load_status_info

# Inputs_search_load_week_filter('Aladdin','NY_ALD_comp_week_filter.csv','NY_Input_ALD_comp_week_filter')

# Inputs_search_load_date_times('Aladdin','NY_ALD_date_times.csv','NY_Input_ALD_date_times')

# Inputs_search_load_DCP_info("Aladdin",'NY_ALD_DCP_info.csv','NY_Input_ALD_DCP_info')

# Inputs_search_load_dynm_info('Aladdin','NY_ALD_dynm_info.csv','NY_Input_ALD_dynm_info')

# Inputs_search_load_rate_info('Aladdin','NY_ALD_group_rate_info.csv','NY_Input_ALD_group_rate_info')

# Inputs_search_load_opt_const('Aladdin','NY_ALD_opt_const.csv','NY_Input_ALD_opt_const')

# Inputs_search_load_diff_const('Aladdin','NY_ALD_price_diff_const.csv','NY_Input_ALD_price_diff_const')

# Inputs_search_load_grid_const('Aladdin','NY_ALD_price_grid_const.csv','NY_Input_ALD_price_grid_const')

# Inputs_search_load_level_info('Aladdin','NY_ALD_price_level_info.csv','NY_Input_ALD_price_level_info')

# Inputs_search_load_maps_past('Aladdin','NY_ALD_price_level_maps_past.csv','NY_Input_ALD_price_level_maps_past')

# Inputs_search_load_maps_raw('Aladdin','NY_ALD_price_level_maps_raw.csv','NY_Input_ALD_price_level_maps_raw')

# Inputs_search_load_tier_info('Aladdin','NY_ALD_price_tier_info.csv','NY_Input_ALD_price_tier_info')

# Inputs_search_load_qualifier_info('Aladdin','NY_ALD_qualifier_info.csv','NY_Input_ALD_qualifier_info')

# Inputs_search_load_perf_list('Aladdin','NY_ALD_refresh_perf_list.csv','NY_Input_ALD_refresh_perf_list')

# Inputs_search_load_id_info('Aladdin','NY_ALD_seat_block_id_info.csv','NY_Input_ALD_seat_block_id_info')

# Inputs_search_load_id_maps('Aladdin','NY_ALD_seat_block_id_maps.csv','NY_Input_ALD_seat_block_id_maps')

# Inputs_search_load_nums_maps('Aladdin','NY_ALD_seat_num_maps.csv','NY_Input_ALD_seat_num_maps')

# Inputs_search_load_row_maps('Aladdin','NY_ALD_seat_row_maps.csv','NY_Input_ALD_seat_row_maps')

# Inputs_search_load_status_info('Aladdin','NY_ALD_status_info.csv','NY_Input_ALD_status_info')

# print(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))

file_date = Marquee_search_file_date('ALADDINAUDIT.TXT')
date_to_delete = datetime.strptime(file_date.lower(), '%d-%b-%y')
print(date_to_delete)
print(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
print(file_date)
print('{:%d-%b-%y}'.format(datetime.now()).upper())