
#Install pip install pysftp==0.2.8. 0.2.9 is still in beta
#Install pip install pypiwin32
#pip install psycopg2
#pip install pandas
#pip3 install sqlalchemy
#pip install xlrd

from sqlalchemy import create_engine,Integer, String
import pysftp
import win32com.client as win32
import time
import pandas as pd

myHostname = "filetransfer.disney.com"
myUsername = 'dtp_clients'
myPassword = 'dtp*890'

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'jude.toussaint@disney.com'
mail.Subject = 'Message subject'
mail.Body = 'Jude, the file is not there'
#mail.CC = "more email addresses here"
#mail.BCC = "more email addresses here"


mail1 = outlook.CreateItem(0)
mail1.To = 'jude.toussaint@disney.com'
mail1.Subject = 'Dont panic but'
mail1.Body = 'The file is definitely not there'



def load_to_db(filename, table_name):

	with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, port =22007) as sftp:
		sftp.cwd('/.')
		list_dir = sftp.listdir()
    #print(list_dir)


# if sftp.exists('TLK.txt')==True:
	#Downloadfile

	#  remotefilepath = '/TLK.txt'
	#  localfilepat = './TLK.txt'

	# sftp.get(remotefilepath, localfilepath)

	#sftp.rename(remote_src, remote_dest): #To rename the file
	#"03_02_2020_ALADDINAUDIT.TT"
		if filename in list_dir:
			print("It's there")#Or download to S3
			remotefilepath = '/'+filename
			localfilepath = './'+filename
			sftp.get(remotefilepath, localfilepath)
			#Marquee File
			df = pd.read_csv(filename,sep='\t')
			engine = create_engine('postgresql://svc_dtg_di:L3REe202x7Q@ddsi-media-dev.cs58lxlzhipp.us-east-1.rds.amazonaws.com:5432/ddsi_dtg', echo=True)
			df.to_sql(table_name,if_exists = 'replace', con=engine, chunksize=1000, schema='raw',index=False, 
				dtype={"EVENT_CODE": String(),'XNUM':String(),'SECTION':String(), 'FROM_ROW':String(),'TO_ROW':String(),'FROM_SEAT':String(),'TO_SEAT':String(),
                'TICKETS':Integer(),'TRANSACTION_DATE':String(),'TRANSACTION_TIME':String(),'FROM_STATUS':String(), 'TO_STATUS':String(),
                'QUALIFIERS':String(),'ACCOUNT':String(),'TRANSACTION_VALUE':Integer(),'OPCODE':String(), 'PRICE_LEVEL':Integer(),
                'SERVICE_CHARGE':Integer(), 'FACILITY_CHARGE':Integer()})
			#send an email


		else:
		#print("Not there")#send an email
			mail.Send()

			r = 0

			while r < 10:
				if filename in sftp.listdir():#Here I need to wrte exactly sftp.listdir() because we need to recheck
					print("It's fnally here")#Download to S3. Send another email
					remotefilepath = '/'+filename
					localfilepath = './'+filename
					sftp.get(remotefilepath, localfilepath)

					#MarqueeFile

					df = pd.read_csv(filename,sep='\t')
					engine = create_engine('postgresql://svc_dtg_di:L3REe202x7Q@ddsi-media-dev.cs58lxlzhipp.us-east-1.rds.amazonaws.com:5432/ddsi_dtg', echo=True)
					df.to_sql(table_name,if_exists = 'replace', con=engine, chunksize=1000, schema='raw',index=False, 
						dtype={"EVENT_CODE": String(),'XNUM':String(),'SECTION':String(), 'FROM_ROW':String(),'TO_ROW':String(),
						'FROM_SEAT':String(),'TO_SEAT':String(),'TICKETS':Integer(),'TRANSACTION_DATE':String(),'TRANSACTION_TIME':String(),
						'FROM_STATUS':String(), 'TO_STATUS':String(),'QUALIFIERS':String(),'ACCOUNT':String(),'TRANSACTION_VALUE':Integer(),
						'OPCODE':String(), 'PRICE_LEVEL':Integer(),'SERVICE_CHARGE':Integer(), 'FACILITY_CHARGE':Integer()})

					#send an emal

				else:
					r+=1				
					print("we ran this " + str(r)+ ' times')#This will be deleted
					time.sleep(5)
					continue

			if r==10:#or time ==5:00PM
				mail1.Send()

	
				
load_to_db('LionKing_20200309.txt','Trans_LionKing_latest_data')
load_to_db('Disney_20200309.txt','Trans_Aladdin_latest_data')
load_to_db('Frozen_20200309.txt','Trans_Frozen_Latest_data')	

				
	#if(r == 10):
		#mail1.send()


