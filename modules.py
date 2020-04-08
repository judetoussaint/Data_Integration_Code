import pysftp
import pandas as pd
from sqlalchemy import create_engine, Integer, String, Time, Float, DateTime, Date, TIMESTAMP
from configparser import ConfigParser
import win32com.client as win32
import time
import pandas as pd
import re,os
import pandas as pd
import numpy as np
import send2trash
import sys
from datetime import datetime, timedelta, date


parser = ConfigParser()
parser.read('dev.ini')

# engine = get_conn()


def get_conn():
	""" gets postgres connection """
	# set connection string
	conn = create_engine('postgresql://'+ parser.get('db','username')+
	':'+parser.get('db','password')+'@'+ parser.get('db','host') +
	':' +str(parser.getint('db','port'))+'/'+parser.get('db','database'), echo=True)
	 
	return conn



def truncate_table_name(schema,table_name):
	engine = get_conn()
	engine.execute('''truncate {0}."{1}"'''.format(schema,table_name))


def process_control_start_end_date(process_name):
	"""This function will get the start_date and end_date from the process control table"""
	engine=get_conn()
	start_date="""select process_start_date from control.process_control where process_name ='{0}'""".format(process_name)
	end_date = """select process_end_date from control.process_control where process_name ='{0}'""".format(process_name)
	process_start_date = pd.read_sql(start_date, engine).to_string().replace('0  ','').replace('process_start_date','').strip()
	process_end_date =pd.read_sql(end_date, engine).to_string().replace('0  ','').replace('process_end_date','').strip()
	return(process_start_date,process_end_date)


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
	


def purge_bad_data(hist_tablename,process_name,showname):
	"""This function is to purge/delete all the data that are needed to be purged from the dates that are in the process table"""
	engine = get_conn()
	engine.execute("""Delete from raw.{0} where transaction_date in {1}""".format(hist_tablename,process_control_in_between_dates(process_name)))
	get_date = process_control_start_end_date(process_name)
	sdate = (datetime.strptime(get_date[0], '%Y-%m-%d'))   # start date
	edate = (datetime.strptime(get_date[1], '%Y-%m-%d'))   # end date
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = "{}".format(alert_emails('15'))
	mail.Subject = "{}".format(alert_subject('15'))
	formatted_body = alert_body('15')
	mail.Body = "{}".format(formatted_body.format(show=showname, purge_start_Date=sdate,purge_end_date=edate))
	mail.Send()
	

def Inputs_search_load_alerts(filename, table_name):

	with pysftp.Connection(host=parser.get('FTP', 'myHostname'), username=parser.get('FTP', 'myUsername'),
		password=parser.get('FTP', 'myPassword'), port=parser.getint('FTP', 'myPort')) as sftp:
		sftp.cwd('/./Manual_Inputs')
		list_dir = sftp.listdir()

		if filename in list_dir:
			print('file is there')
			remotefilepath = '/Manual_Inputs/'+filename
			localfilepath = './'+filename
			sftp.get(remotefilepath, localfilepath)
			df = pd.read_csv(filename)
			engine = get_conn()
			df.to_sql(table_name, if_exists='replace', con=engine,
					  chunksize=1000, index=False, schema='raw')



def Marquee_search_file_date(filename):

	with pysftp.Connection(host=parser.get('FTP', 'myHostname'), username=parser.get('FTP', 'myUsername'),
		password=parser.get('FTP', 'myPassword'), port=parser.getint('FTP', 'myPort')) as sftp:
		sftp.cwd('/.')
		remotefilepath = '/'+filename
		localfilepath = './'+filename
		sftp.get(remotefilepath, localfilepath)
		with open(filename) as file_object:
			contents = file_object.read().replace('\n', ';')
			regex = r'TICKETMASTER.+?\bSEATS\b'
			important_list = re.findall(regex, contents)
	date = (important_list[0].split(';')[0][51:61].strip())
	return date



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




def transform_raw(filename):

	with open(filename) as file_object:
		contents = file_object.read().replace('\n', ';')
	regex = r'TICKETMASTER.+?\bSEATS\b'
	important_list = re.findall(regex, contents)

	second_data_loop = pd.DataFrame()
	for i in range(len(important_list)):

		imp_list = important_list[i].split(';')
		evcode = pd.Series([imp_list[0][31:40].strip()])
		date = pd.Series([imp_list[0][51:61].strip()])
		time = pd.Series([imp_list[0][61:68].strip()])
		PL = pd.Series(imp_list[8].split()[1:-2])
		first_data_loop = pd.DataFrame()
		for j in range(9, len(imp_list)-2):
		# remember here imp_list is important_list[0]
			Price = pd.Series(imp_list[j].split()[1:])
			Level = pd.Series(imp_list[j].split()[0])
			data = pd.concat([evcode, date, time, PL, Level,
							 Price], axis=1).fillna(method='ffill')
			first_data_loop = first_data_loop.append(data, ignore_index=True)
		second_data_loop = second_data_loop.append(
			first_data_loop, ignore_index=True)
	second_data_loop.columns = [
		'evcode', 'file_date', 'file_time', 'pl', 'level', 'price']
	second_data_loop['price'] = pd.to_numeric(
		second_data_loop['price'], errors='coerce')

	return second_data_loop


# that_date = Marquee_search_file_date('ALADDINAUDIT.TXT')
# print(that_date)


def Marquee_search_transform_load(filename, table_name,show_name):#I delete the table here, and reupload with "truncate" and "Append"
	file_date = Marquee_search_file_date(filename)#this argument comes from the top argument filename
	today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
	today_1 = '{:%d-%b-%y}'.format(datetime.now()).upper()
	date_to_delete = datetime.strptime(file_date.lower(), '%d-%b-%y')
	# date_to_delete = 'hi'#delete this
	# if date_to_delete == 'hi':#delete this
	if date_to_delete == today:
		df = transform_raw(filename)
		df['status'] = 'Normal Process'
		df['run_date'] = '{:%d-%b-%y}'.format(datetime.now()).upper()
		df = df[['evcode', 'file_date', 'file_time', 'run_date', 'status','pl','level','price']]
		engine = get_conn()
		# truncate_table_name('raw',table_name)#I delete the table here

		df.to_sql(table_name, if_exists='replace', con=engine, chunksize=1000, schema='raw', index=False,
		dtype={"evcode": String(), "file_date": Date(), "file_time": Time(), 'pl': String(), 'level': String(), 
		'price': Float(),'status':String(),'run_date':Date()})

		outlook = win32.Dispatch('outlook.application')
		mail = outlook.CreateItem(0)
		mail.To = "{}".format(alert_emails('2'))
		mail.Subject = "{}".format(alert_subject('2'))
		formatted_body = alert_body('2')
		mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=file_date))
		mail.Send()
		os.remove(filename)
		# engine.execute(""" delete  from raw."{0}" 
		# where run_date ='{1}'""".format(hist_table_name,date_to_delete))
		# print('it done')




		#and send it to the database
	else:
		outlook = win32.Dispatch('outlook.application')
		mail = outlook.CreateItem(0)
		mail.To = "{}".format(alert_emails('1'))
		mail.Subject = "{}".format(alert_subject('1'))
		formatted_body = alert_body('1')
		mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=file_date, today=today_1))
		mail.Send()
		os.remove(filename)#I send it to trash because we don't want to have two files with same name
		r = 0

		while r < 10:
			file_date1 = Marquee_search_file_date(filename)
			if file_date1 == today:
				df = transform_raw(filename)
				df['status'] = 'Normal Process'
				df['run_date'] = '{:%d-%b-%y}'.format(datetime.now()).upper()
				df = df[['evcode', 'file_date', 'file_time', 'run_date', 'status','pl','level','price']]
				engine = get_conn()
				# truncate_table_name('raw',table_name)
				df.to_sql(table_name, if_exists='replace', con=engine, chunksize=1000, schema='raw', index=False,
					dtype={"evcode": String(), "file_date": Date(), "file_time": Time(), 'pl': String(), 'level': String(),
					 'price': Float(),'status':String(),'run_date':Date()})
				os.remove(filename)
				#and send an email to mark completion
				# engine.execute(""" delete  from raw."{0}" 
				# where run_date ='{1}'""".format(hist_table_name,date_to_delete))
				# print('it done')
			else:
				r+=1
				print("we ran this " + str(r) + ' times')
				time.sleep(5)
				continue

		if r == 10 or datetime.datetime.now().strftime("%I:%M:%S %p") == '04:30:00 PM':
			print('file is definitely not there')



def marquee_backup(table_name,hist_table_name,show_name):
	truncate_table_name('raw',table_name)
	engine = get_conn()
	# engine1 = get_conn()
	engine.execute('''insert into raw."{0}"select event_code , file_date ,file_time ,(select current_date) as run_date,
	(select 'backup process' as status),pl,"levels",price from raw."{1}" where file_date = (select max(file_date)
	from raw.{1})'''.format(table_name,hist_table_name)
	)
	query = '''select max(file_date) from raw.ny_ald_hist_marquee_prices nahmp '''
	file_date = pd.read_sql(query, engine).to_string().replace('0  ','').replace('max','')
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = "{}".format(alert_emails('3'))
	mail.Subject = "{}".format(alert_subject('3'))
	formatted_body = alert_body('3')
	mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=file_date))
	mail.Send()
	




def marquee_reprocess(filename, table_name, show_name,process_name):#I delete the table here, and reupload with "truncate" and "Append"
	file_date = Marquee_search_file_date(filename)
	today = '{:%d-%b-%y}'.format(datetime.now()).upper()# I may need to add this line --if (process_indicator(process_name)== 'Y')
	if file_date == today and (process_indicator(process_name)== 'Y'):
		df = transform_raw(filename)
		df['status'] = 'Reprocess'
		df['run_date'] = '{:%d-%b-%y}'.format(datetime.now()).upper()
		df = df[['evcode', 'file_date', 'file_time', 'run_date', 'status','pl','level','price']]
		engine = get_conn()
		# truncate_table_name('raw',table_name)#I delete the table here

		df.to_sql(table_name, if_exists='replace', con=engine, chunksize=1000, schema='raw', index=False,
		dtype={"evcode": String(), "file_date": Date(), "file_time": Time(), 'pl': String(), 'level': String(), 
		'price': Float(),'status':String(),'run_date':Date()})

		outlook = win32.Dispatch('outlook.application')
		mail = outlook.CreateItem(0)
		mail.To = "{}".format(alert_emails('7'))
		mail.Subject = "{}".format(alert_subject('7'))
		formatted_body = alert_body('7')
		mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=file_date))
		mail.Send()
		engine.execute("""update control.process_control set process_indicator = 'N' where process_name = {0}""".format(process_name))


		#and send it to the database
	else:
		print("the date is still not right")





def ActorsFund_search_transform_load(filename, table_name, show_name,process_name):#I delete the table here, and reupload with "truncate" and "Append"
	get_date = process_control_start_end_date(process_name)
	end_date = (datetime.strptime(get_date[1], '%Y-%m-%d'))
	start_date = (datetime.strptime(get_date[0], '%Y-%m-%d'))
	# start_date < datetime.now() < end_date
	file_date = Marquee_search_file_date(filename)#this argument comes from the top argument filename
	today = '{:%d-%b-%y}'.format(datetime.now()).upper()
	if process_indicator(process_name)== 'Y' and start_date <= datetime.now() <= end_date and file_date == today: 
		df = transform_raw(filename)
		df['status'] = 'Normal Process'
		df['run_date'] = '{:%d-%b-%y}'.format(datetime.now()).upper()
		df = df[['evcode', 'file_date', 'file_time', 'run_date', 'status','pl','level','price']]
		engine = get_conn()
		# truncate_table_name('raw',table_name)#I delete the table here

		df.to_sql(table_name, if_exists='replace', con=engine, chunksize=1000, schema='raw', index=False,
		dtype={"evcode": String(), "file_date": Date(), "file_time": Time(), 'pl': String(), 'level': String(), 
		'price': Float(),'status':String(),'run_date':Date()})

		outlook = win32.Dispatch('outlook.application')
		mail = outlook.CreateItem(0)
		mail.To = "{}".format(alert_emails('5'))
		mail.Subject = "{}".format(alert_subject('5'))
		formatted_body = alert_body('5')
		mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=file_date))
		mail.Send()
		send2trash.send2trash(filename)
		engine.execute("""update control.process_control 
					set process_indicator = 'N'
					where process_name = '{}'""".format(process_name)
					)




		#and send it to the database
	else:
		outlook = win32.Dispatch('outlook.application')
		mail = outlook.CreateItem(0)
		mail.To = "{}".format(alert_emails('4'))
		mail.Subject = "{}".format(alert_subject('4'))
		formatted_body = alert_body('4')
		mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=file_date, today=today))
		mail.Send()
		send2trash.send2trash(filename)#I send it to trash because we don't want to have two files with same name
		r = 0

		while r < 10:
			file_date1 = Marquee_search_file_date(filename)
			if file_date1 == today:
				df = transform_raw(filename)
				df['status'] = 'Normal Process'
				df['run_date'] = '{:%d-%b-%y}'.format(datetime.now()).upper()
				df = df[['evcode', 'file_date', 'file_time', 'run_date', 'status','pl','level','price']]
				engine = get_conn()
				# truncate_table_name('raw',table_name)
				df.to_sql(table_name, if_exists='replace', con=engine, chunksize=1000, schema='raw', index=False,
					dtype={"evcode": String(), "file_date": Date(), "file_time": Time(), 'pl': String(), 'level': String(),
					 'price': Float(),'status':String(),'run_date':Date()})
				#and send an email to mark completion

			else:
				r+=1
				print("we ran this " + str(r) + ' times')
				time.sleep(5)
				continue

		if r == 10 or datetime.datetime.now().strftime("%I:%M:%S %p") == '04:30:00 PM':
			print('file is definitely not three')



def ActorsFund_backup(table_name,hist_table_name,show_name):
	truncate_table_name('raw',table_name)
	engine = get_conn()
	# engine1 = get_conn()
	engine.execute('''insert into raw."{0}"select event_code , file_date ,file_time ,(select current_date) as run_date,
	(select 'backup process' as status),pl,"levels",price from raw."{1}" where file_date = (select max(file_date)
	from raw.{1})'''.format(table_name,hist_table_name)
	)
	query = '''select max(file_date) from raw.ny_ald_hist_marquee_prices nahmp '''
	file_date = pd.read_sql(query, engine).to_string().replace('0  ','').replace('max','')
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = "{}".format(alert_emails('6'))
	mail.Subject = "{}".format(alert_subject('6'))
	formatted_body = alert_body('6')
	mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=file_date))
	mail.Send()



def ActorsFund_reprocess(filename, table_name, show_name):#I delete the table here, and reupload with "truncate" and "Append"
	file_date = Marquee_search_file_date(filename)
	today = '{:%d-%b-%y}'.format(datetime.now()).upper()
	if file_date == today:
		df = transform_raw(filename)
		df['status'] = 'Reprocess'
		df['run_date'] = '{:%d-%b-%y}'.format(datetime.now()).upper()
		df = df[['evcode', 'file_date', 'file_time', 'run_date', 'status','pl','level','price']]
		engine = get_conn()
		# truncate_table_name('raw',table_name)#I delete the table here

		df.to_sql(table_name, if_exists='replace', con=engine, chunksize=1000, schema='raw', index=False,
		dtype={"evcode": String(), "file_date": Date(), "file_time": Time(), 'pl': String(), 'level': String(), 
		'price': Float(),'status':String(),'run_date':Date()})

		outlook = win32.Dispatch('outlook.application')
		mail = outlook.CreateItem(0)
		mail.To = "{}".format(alert_emails('7'))
		mail.Subject = "{}".format(alert_subject('7'))
		formatted_body = alert_body('7')
		mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=file_date))
		mail.Send()
	


		#and send it to the database
	else:
		print("the date is still not right")




# def load_actors_fund_tlk():
# 	"""If you call this function it will load the tlk actors fund at the right moment"""

# 	get_date = process_control_start_end_date('Actors Fund')
# 	end_date = (datetime.strptime(get_date[1], '%Y-%m-%d'))
# 	start_date = (datetime.strptime(get_date[0], '%Y-%m-%d'))

# 	if start_date < datetime.now() < end_date :

# 		ActorsFund_search_transform_load('TLKACTORSFUND.TXT','ny_actorsf_tlk_latest_data','LionKing')



# def load_actors_fund_frz():

# 	get_date = process_control_start_end_date('Actors Fund')
# 	end_date = (datetime.strptime(get_date[1], '%Y-%m-%d'))
# 	start_date = (datetime.strptime(get_date[0], '%Y-%m-%d'))

# 	if start_date < datetime.now() < end_date :

# 		ActorsFund_search_transform_load('FRZACTORSFUND.TXT','ny_actorsf_frz_latest_data','Frozen')



# def load_actors_fund_ald():

# 	get_date = process_control_start_end_date('Actors Fund')
# 	end_date = (datetime.strptime(get_date[1], '%Y-%m-%d'))
# 	start_date = (datetime.strptime(get_date[0], '%Y-%m-%d'))

# 	if start_date < datetime.now() < end_date :

# 		ActorsFund_search_transform_load('ALADDINACTORSFUND.TXT','ny_actorsf_ald_latest_data','Aladdin')




def transaction_search_load(filename, table_name,show_name):

	with pysftp.Connection(host=parser.get('FTP', 'myHostname'), username=parser.get('FTP', 'myUsername'),
		password=parser.get('FTP', 'myPassword'), port=parser.getint('FTP', 'myPort')) as sftp:
		sftp.cwd('/.')
		list_dir = sftp.listdir()
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
				df['status'] = 'Normal Process'
				df.columns =['event_code','xnum','section','from_row','to_row','from_seat','to_seat',
				'tickets','transaction_date','transaction_time','from_status','to_status','qualifiers','account','transaction_value',
				'opcode','price_level','service_charge','facility_charge','run_date','status']		
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
				mail.To = "{}".format(alert_emails('9'))
				mail.Subject = "{}".format(alert_subject('9'))
				formatted_body = alert_body('9')
				mail.Body = "{}".format(formatted_body.format(show=show_name, file_date=date))#We might need to change this date
				mail.Send()


		else:
			print("It is not there. I will send email")#send an email
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('8'))
			mail.Subject = "{}".format(alert_subject('8'))
			formatted_body = alert_body('8')
			mail.Body = "{}".format(formatted_body.format(show=show_name, file_name=filename))
			mail.Send()
	

			r = 0

			while r < 10:
				if filename in sftp.listdir():#Here I need to wrte exactly sftp.listdir() because we need to recheck
					print("It's fnally here")#Download to S3. Send another email
					remotefilepath = '/'+filename
					localfilepath = './'+filename
					sftp.get(remotefilepath, localfilepath)
					df = pd.read_csv(filename,sep='\t')
					# Transaction_read_load()

					if len(df) == 0:
						print('file is empty')
						outlook = win32.Dispatch('outlook.application')
						mail = outlook.CreateItem(0)
						mail.To = "{}".format(alert_emails('14'))
						mail.Subject = "{}".format(alert_subject('14'))
						formatted_body = alert_body('14')
						mail.Body = "{}".format(formatted_body.format(show=show_name,file_name =filename, file_date=date))
						mail.Send()
						print('File is empty')
						#maybe send an email
					else:					
						# dialect+driver://username:password@host:port/database
						df = pd.read_csv(filename,sep='\t')
						df['run_date'] = '{:%d-%b-%y}'.format(datetime.now()).upper()
						df['status'] = 'Normal Processing'
						df.columns =['event_code','xnum','section','from_row','to_row','from_seat','to_seat',
						'tickets','transaction_date','transaction_time','from_status','to_status','qualifiers','account','transaction_value',
						'opcode','price_level','service_charge','facility_charge','run_date','status']
						engine = get_conn()
						df.to_sql(table_name,if_exists = 'replace', con=engine, chunksize=1000, schema='raw',index=False, 
							dtype={"event_code": String(),'xnum':Float(),'section':String(), 'from_row':String(),'to_row':String(),'from_seat':Integer(),'to_seat':Integer(),
							'tickets':Integer(),'transaction_date':Date(),'transaction_time':String(),'from_status':String(), 'to_status':String(),
							'qualifiers':String(),'account':String(),'transaction_value':Integer(),'opcode':String(), 'price_level':Integer(),
							'service_charge':Integer(), 'facility_charge':Integer(),'run_date':Date(),'status':String()})
					# send an emal

				else:
					r+=1				
					print("we ran this " + str(r)+ ' times')#This will be deleted
					time.sleep(5)
					continue

			if r==10 or datetime.datetime.now().strftime("%I:%M:%S %p") == '04:30:00 PM':#or time ==5:00PM
				print("File definitely not there")
				outlook = win32.Dispatch('outlook.application')
				mail = outlook.CreateItem(0)
				mail.To = "{}".format(alert_emails('10'))
				mail.Subject = "{}".format(alert_subject('10'))
				formatted_body = alert_body('10')
				mail.Body = "{}".format(formatted_body.format(show=show_name, file_name=filename))
				mail.Send()
	




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


#This is what I have in mind for Monday
def trans_file_to_load(tablename,show_name,hist_table_name):#Maybe I should replace the order
	file_lists = trans_files_to_search(show_name,hist_table_name)#Now it's only searching for Disney.it used to be empty like trans_files_to_search()
	for file_name in file_lists:
		transaction_search_load(file_name,tablename,show_name)

		#second step
		delete_recent_date_Trans(hist_table_name,tablename)#Maybe I can add those tables as arguments in the table

		#third step
		insert_recent_data_into_hist(hist_table_name,tablename)

# dialect+driver://username:password@host:port/database





##############     REPROCESS      ###############
def transaction_reprocess_all(table_name,show_name,process_name, hist_tablename):#Requirement 6.0
	"""This function reprocess all the transaction files given that  process_indicator='Y' and
	today's date is greater than process_end_date"""
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

	show_list = []
	for i in range(len(a)):
		show_list.append(show_name +'_' + a[i].split()[0].replace('-','')+'.txt')

	return(show_list)






def transaction_reprocess_search_load(filename, table_name,show_name):
	"""This function is to reprocess a transaction file. Major difference to transaction_search_load
	is the status='Reprocess' and the email's difference"""

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
		





##############SQL_TRANSFORM###############


def latest_marquee_prices(table_name,existing_table_1,existing_table_2):
	truncate_table_name('raw',table_name)
	engine = get_conn()
	engine.execute( '''Insert into raw."{0}"(select distinct a.* from raw."{1}" as a 
	left join raw."{2}" as b on a.evcode = b.event_code 	
	where b.show_date >= a.file_date - 2 or b.show_date is null)'''.format(table_name,existing_table_1,existing_table_2))
	print('It is done')
	

def delete_recent_date_Marq(hist_table_name,recent_table_name):
	engine = get_conn()
	engine.execute(''' delete  from raw."{0}" 
	where run_date =(select max(file_date) from raw."{1}")'''.format(hist_table_name,recent_table_name))
	print('it done')


def delete_recent_date_Trans(hist_table_name,recent_table_name):
	engine = get_conn()
	engine.execute(''' delete from raw.{0} 
	where transaction_date =(select max(transaction_date) from raw.{1})'''.format(hist_table_name,recent_table_name))
	print('it done')


def insert_recent_data_into_hist(hist_table_name,recent_table_name):
	engine = get_conn()
	engine.execute('''insert into raw.{0} select * from raw.{1}'''.format(hist_table_name,recent_table_name))
	print('really done')







##############EMAILS    &  INDICATOR#################



def alert_emails(number):
	engine = get_conn()
	query = """select string_agg(email, ';') from 
	(select first_tables.*,al.location, al.type,al.subject, al.headline, al.body from
	(select ral.role, ral.role_type, ral.alert,erl.name,erl.email from raw.role_alert_list ral
	inner join raw.email_role_list erl on ral."role" = erl."role")first_tables
	inner join raw.alert_list al on first_tables.alert = al.alert)as all_tables
	where all_tables.alert= 'alert_{}' """.format(number)
	emails = pd.read_sql(query, engine).to_string().replace('0  ','').replace('string_agg','').strip()
	return emails


def alert_body(number):
	engine = get_conn()
	query = '''select distinct body from 
	(select first_tables.*,al.location, al.type,al.subject, al.headline, al.body from
	(select ral.role, ral.role_type, ral.alert,erl.name,erl.email from raw.role_alert_list ral
	inner join raw.email_role_list erl on ral."role" = erl."role")first_tables
	inner join raw.alert_list al on first_tables.alert = al.alert)as all_tables
	where all_tables.alert= 'alert_{}' '''.format(number)
	formatted_body = pd.read_sql(query,engine).to_string().replace('0  ','').replace('body','')
	# body = formatted_message.format(show= show_name,file_date=file_date)
	return formatted_body



def alert_subject(number):
	engine = get_conn()
	query = """select distinct subject from 
	(select first_tables.*,al.location, al.type,al.subject, al.headline, al.body from
	(select ral.role, ral.role_type, ral.alert,erl.name,erl.email from raw.role_alert_list ral
	inner join raw.email_role_list erl on ral."role" = erl."role")first_tables
	inner join raw.alert_list al on first_tables.alert = al.alert)as all_tables
	where all_tables.alert= 'alert_{}' """.format(number)
	subject = pd.read_sql(query, engine).to_string().replace('0  ','').replace('subject','').strip()
	return subject

def process_indicator(processname):
	engine = get_conn()
	query = """select process_indicator from control.process_control where process_name='{}'""".format(processname)
	result = pd.read_sql(query, engine).to_string().replace('0  ','').replace('process_indicator','').strip()
	return result



# outlook = win32.Dispatch('outlook.application')
# mail = outlook.CreateItem(0)
# mail.To = "{}".format(alert_emails('13'))
# mail.Subject = "{}".format(alert_subject('5'))
# mail.Body = "{}".format(alert_message('5','ALADDINAUDIT.TXT','ALADDIN'))
# mail.CC = "jude.toussaint@disney.com;Carlos.A.Cocuy@disney.com"
# mail.BCC = "more email addresses here"


# # mail1 = outlook.CreateItem(0)
# # mail1.To = 'jude.toussaint@disney.com'
# # mail1.Subject = 'Dont panic but'
# # mail1.Body = 'The file is definitely not there'

# # mail2 = outlook.CreateItem(0)
# # mail2.To = 'jude.toussaint@disney.com'
# # mail2.Subject = 'Dont panic but'
# # mail2.Body = 'The file is definitely not there'

# # mail3 = outlook.CreateItem(0)
# # mail3.To = 'jude.toussaint@disney.com'
# # mail3.Subject = 'Dont panic but'
# # mail3.Body = 'The file is definitely not there'

# # mail4 = outlook.CreateItem(0)
# # mail4.To = 'jude.toussaint@disney.com'
# # mail4.Subject = 'Dont panic but'
# # mail4.Body = 'The file is definitely not there'

# # mail5 = outlook.CreateItem(0)
# # mail5.To = 'jude.toussaint@disney.com'
# # mail5.Subject = 'Dont panic but'
# # mail5.Body = 'The file is definitely not there'


	







