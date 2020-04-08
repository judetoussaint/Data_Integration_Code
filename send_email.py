import win32com.client as win32
from modules import alert_body,alert_emails,alert_subject,get_conn,transaction_search_load
from Sql_Transform import delete_recent_date_Trans, insert_recent_data_into_hist
import pandas as pd
from datetime import datetime,timedelta
from configparser import ConfigParser
import pysftp
parser = ConfigParser()
parser.read('dev.ini')


# outlook = win32.Dispatch('outlook.application')
# mail = outlook.CreateItem(0)
# mail.To = "{}".format(alert_emails('3'))#"jude.toussaint@disney.com;Carlos.A.Cocuy@disney.com"
# mail.Subject = 'Message subject'
# mail.Body = 'Jude, the file is not there'
# # mail.CC = "jude.toussaint@disney.com;Carlos.A.Cocuy@disney.com"
# # mail.BCC = "more email addresses here"
# mail.send


#Visual Studio Code VS Terminal
# a ='{}'.format(alert_emails('3'))#"jude.toussaint@disney.com;Carlos.A.Cocuy@disney.com"
# print(a)
# # print(f"{alert_emails('3')}")
# print('Carlos.A.Cocuy@disney.com;Jude.Toussaint@disney.com')

# from datetime import date
# d1 = date(2011, 3, 28)
# print(d1)
# print(str(d1))
# print(type(d1))

# d2 = date('2020-01-01')

# today = '{:%d-%b-%y}'.format(datetime.now()).upper()
# print(today)
# print(type(today))


def process_control_date():
	engine=get_conn()
	start_date='''select process_start_date from control.process_control'''
	end_date = '''select process_end_date from control.process_control'''
	process_start_date = pd.read_sql(start_date, engine).to_string().replace('0  ','').replace('process_start_date','').strip()
	process_end_date =pd.read_sql(end_date, engine).to_string().replace('0  ','').replace('process_end_date','').strip()
	return(process_start_date,process_end_date)
	# df = alert_emails_try('3')
# print(df)

get_date = process_control_date()
# print(get_date)
# print(datetime.now())

# end_date = (datetime.strptime(get_date[1], '%Y-%m-%d'))
# start_date = (datetime.strptime(get_date[0], '%Y-%m-%d'))

# if start_date < datetime.now() < end_date :
#     print("It's between")


def start_trans_date(hist_table_name):#Add a parameter here
	'''The earliest date to start looking for in Transaction file
	It's maximum date in the table + 1'''
	 
	engine=get_conn()
	date='''select max(transaction_date) from raw.{0}'''.format(hist_table_name)
	max_date_string = pd.read_sql(date, engine).to_string().replace('0  ','').replace('max','').strip().replace('-','')
	max_date_datetime =(datetime.strptime(max_date_string, '%Y%m%d'))
	max_date_date_plus1day= max_date_datetime + timedelta(1)
	return '{:%Y%m%d}'.format(max_date_date_plus1day)
	



def list_files_on_FTP():
	'''This function is just getting the list of files on SFTP. I did not use it, but may come handy in the future'''
	with pysftp.Connection(host=parser.get('FTP', 'myHostname'), username=parser.get('FTP', 'myUsername'),
		password=parser.get('FTP', 'myPassword'), port=parser.getint('FTP', 'myPort')) as sftp:
		sftp.cwd('/.')
		list_dir = sftp.listdir()
		return (list_dir)

 
def trans_files_to_search(show_name,hist_table_name):
	'''This function is creaating a list of files that needs to be loaded. Last date to load is yesterday file'''
	get_date = start_trans_date(hist_table_name)#Here I am looking for the date to start looking for files. It's the last date in the databs plus 1 day

	start_date = datetime.strptime(get_date, '%Y%m%d')
	end_date = datetime.strptime('{:%Y%m%d}'.format(datetime.now()-timedelta(1)),'%Y%m%d') #It's yesterday

	delta = end_date - start_date       # as timedelta

	date_to_check = []
	for i in range(delta.days + 1):
		day = start_date + timedelta(days=i)
		date_to_check.append(day.strftime('%Y%m%d')) #Here I am looking for a range of dates

		file_to_check = [] #Here I am adding the showname to the different dates
		for j in date_to_check:
			file_to_check.append(show_name+'_'+j+'.txt')#Python 3.8 may be acting up in the append
			#Hey Jude where you see showname. It was Disney at first

	# list_FTP_files = list_files_on_FTP()#Here I am getting the list of files availables on FTP.
	# files_to_upload = []
	# for file in file_to_check:#Here I want to make sure I only upload files that are available. Because If I don't....
	# 	if file in list_FTP_files:				#....code can keep looking for the file for up to 8 hours and forgo the rest				
	# 		files_to_upload.append(file)
	return(file_to_check)


what_files = trans_files_to_search('Frozen','ny_frz_hist_transaction_data')
print(what_files)


#This is what I have in mind for Monday
def trans_file_to_load(tablename,show_name,hist_table_name):#Maybe I should replace the order
	file_lists = trans_files_to_search(show_name,hist_table_name)#Now it's only searching for Disney.it used to be empty like trans_files_to_search()
	for file_name in file_lists:
		transaction_search_load(file_name,tablename,show_name)

		#second step
		delete_recent_date_Trans(hist_table_name,tablename)#Maybe I can add those tables as arguments in the table

		#third step
		insert_recent_data_into_hist(hist_table_name,tablename)

# trans_file_to_load('ny_trans_ald_latest_data','Disney','ny_ald_hist_transaction_data')
# get_date = start_trans_date('ny_ald_hist_transaction_data')
# end_date = datetime.strptime('{:%Y%m%d}'.format(datetime.now()-timedelta(1)),'%Y%m%d') #It's yesterday
# start_date = datetime.strptime(get_date, '%Y%m%d')
# print(end_date)
# print(get_date)

