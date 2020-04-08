
#String(), Integer(),Float(),Date()
from modules import get_conn,alert_body,alert_emails,alert_subject
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

def Inputs_search_load_week_filter(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'comp_week_name':String(),'comp_week_order':Integer(), 
                    'weeks_prior':Integer(),'start_date':Date(),'end_date':Date()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()
            # send2trash.send2trash('./'+filename)

def Inputs_search_load_date_times(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'perf_id':String(), 
                    'uniq':String(),'event_code':String(),'show_date':Date(),'show_time':Time(),
                    'matinee':Integer(),'broadway_week_ind':Integer(),'off_sale_ind':Integer(),
                    'closed_balc_ind':Integer(),'outlier_ind':Integer(),'onsale_date':Date(),
                    'season':String(),'peak_period_ind':Integer(),'show_week':Integer(),'bp':Integer(),
                    'previews_ind':Integer(),'premier_ind':Integer(),'closing_ind':Integer(),'weekday_ind':Integer(),
                    'weekend_ind':Integer(),'weekday_type':Integer(),'group_rate_list':String(),
                    'py_perf_id_exception':String(),'set_up_like_perf_id':String(),'notes':String()

					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_DCP_info(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'dcp':Integer(), 
                    'end_date':Date()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_dynm_info(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"event_code": String(),'show_date':Date(),'show_time':Time(), 
                    'fee_level':String(),'dynm':String(),'start_date':Date(),'end_date':Date()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_rate_info(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'start_date':Date(), 
                    'end_date':Date(),'group_type_id':String(),'group_rate_id':String(),'group_rate_name':String(),
                    'group_section_list':String(),'group_section_name':String(),'list_group_rate':Float(),
                    'group_rate':Float(),'min_full_price':Integer(),'max_full_price':Integer()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()

def Inputs_search_load_opt_const(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={'location':String(),'show':String(),'price_tier':Integer(),'reln_pt1':Integer(),
                    'reln_pt2':Integer(),'reln_pt3':Integer(),'reln_pt4':Integer(),'reln_pt5':Integer(),
                    'reln_pt6':Integer(),'reln_pt7':Integer(),'reln_pt8':Integer(),'reln_pt9':Integer(),
                    'reln_pt10':Integer(),'reln_pt11':Integer(),'reln_pt12':Integer(),'reln_pt13':Integer(),
                    'reln_pt14':Integer(),'reln_pt15':Integer(),'reln_pt16':Integer(),'reln_pt17':Integer(),
                    'reln_pt18':Integer(),'reln_pt19':Integer(),'reln_pt20':Integer(),'spill_pt1':Integer(),
                    'spill_pt2':Integer(),'spill_pt3':Integer(),'spill_pt4':Integer(),'spill_pt5':Integer(),
                    'spill_pt6':Integer(),'spill_pt7':Integer(),'spill_pt8':Integer(),'spill_pt9':Integer(),
                    'spill_pt10':Integer(),'spill_pt11':Integer(),'spill_pt12':Integer(),'spill_pt13':Integer(),
                    'spill_pt14':Integer(),'spill_pt15':Integer(),'spill_pt16':Integer(),'spill_pt17':Integer(),
                    'spill_pt18':Integer(),'spill_pt19':Integer(),'spill_pt20':Integer(),'const_threshold':Float(),
                    'occ_target_1':Float(),'occ_target_2':Float(),'occ_penalty_1':Integer(),'occ_penalty_2':Integer(),
                    'price_penalty_1':Integer(),'price_penalty_2':Integer(),'cluster_num':Integer(),'start_date':Date(),
                    'end_date':Date()

					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()



def Inputs_search_load_diff_const(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'ref_pt':Integer(),'target_pt':Integer(),
                    'max_price_diff':Integer(),'min_price_diff':Integer(),'start_date':Date(), 
                    'end_date':Date()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_grid_const(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'price_tier':Integer(),'price_floor':Float(),
                    'price_ceiling':Integer(),'max_change':Float(),'start_date':Date(), 
                    'end_date':Date()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_level_info(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'price_level':Integer(),'price_level_name':String(),
                    'price_level_order':Integer(),'price_tier':Integer(),'no_gp_ind':Integer(),
                    'non_seat_ind':Integer(),'group_section_id':String(),'start_date':Date(), 
                    'end_date':Date()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_maps_past(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"grid_row": Integer(),
                    'c1':Integer(),'c2':Integer(),'c3':Integer(),'c4':Integer(),'c5':Integer(),'c6':Integer(),
                    'c7':Integer(),'c8':Integer(),'c9':Integer(),'c10':Integer(),'c11':Integer(),'c12':Integer(),
                    'c13':Integer(),'c14':Integer(),'c15':Integer(),'c16':Integer(),'c17':Integer(),'c18':Integer(),
                    'c19':Integer(),'c20':Integer(),'c21':Integer(),'c22':Integer(),'c23':Integer(),'c24':Integer(),
                    'c25':Integer(),'c26':Integer(),'c27':Integer(),'c28':Integer(),'c29':Integer(),'c30':Integer(),
                    'c31':Integer(),'c32':Integer(),'c33':Integer(),'c34':Integer(),'c35':Integer(),'c36':Integer(),
                    'c37':Integer(),'c38':Integer(),'c39':Integer(),'c40':Integer(),'c41':Integer(),'c42':Integer(),
                    'c43':Integer(),'c44':Integer(),'c45':Integer(),'c46':Integer(),'c47':Integer(),'c48':Integer(),
                    'c49':Integer(),'c50':Integer(),'c51':Integer(),'c52':Integer(),'c53':Integer(),'c54':Integer(),
                    'c55':Integer(),'c56':Integer(),'c57':Integer(),'c58':Integer(),'c59':Integer(),'c60':Integer(),
                    'c61':Integer(),'c62':Integer(),'start_date':Date(),'end_date':Date(),'location':String(),
                    'show':String(),'config_id':Integer()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()



def Inputs_search_load_maps_raw(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"grid_row": Integer(),
                    'c1':Integer(),'c2':Integer(),'c3':Integer(),'c4':Integer(),'c5':Integer(),'c6':Integer(),
                    'c7':Integer(),'c8':Integer(),'c9':Integer(),'c10':Integer(),'c11':Integer(),'c12':Integer(),
                    'c13':Integer(),'c14':Integer(),'c15':Integer(),'c16':Integer(),'c17':Integer(),'c18':Integer(),
                    'c19':Integer(),'c20':Integer(),'c21':Integer(),'c22':Integer(),'c23':Integer(),'c24':Integer(),
                    'c25':Integer(),'c26':Integer(),'c27':Integer(),'c28':Integer(),'c29':Integer(),'c30':Integer(),
                    'c31':Integer(),'c32':Integer(),'c33':Integer(),'c34':Integer(),'c35':Integer(),'c36':Integer(),
                    'c37':Integer(),'c38':Integer(),'c39':Integer(),'c40':Integer(),'c41':Integer(),'c42':Integer(),
                    'c43':Integer(),'c44':Integer(),'c45':Integer(),'c46':Integer(),'c47':Integer(),'c48':Integer(),
                    'c49':Integer(),'c50':Integer(),'c51':Integer(),'c52':Integer(),'c53':Integer(),'c54':Integer(),
                    'c55':Integer(),'c56':Integer(),'c57':Integer(),'c58':Integer(),'c59':Integer(),'c60':Integer(),
                    'c61':Integer(),'c62':Integer(),'start_date':Date(),'end_date':Date(),'location':String(),
                    'show':String(),'config_id':Integer()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_tier_info(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'price_tier':Integer(),'price_tier_name':String(),
                    'price_tier_order':Integer(),'no_forecast_ind':Integer(),
                    'start_date':Date(), 
                    'end_date':Date()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_qualifier_info(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'qualifier':String(),'qualifier_type':String(),
                    'start_date':Date(), 
                    'end_date':Date()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()

def Inputs_search_load_perf_list(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"perf_id": String(),'curr_dcp':Integer(),
                    'effective_date':Date()
                    
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_id_info(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'seat_block_id':String(),'seat_block_id_name':String(),
                    'seat_block_id_order':Integer(),'start_date':Date(),'end_date':Date()
                                       
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_id_maps(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"grid_row": Integer(),
                    'c1':String(),'c2':String(),'c3':String(),'c4':String(),'c5':String(),'c6':String(),
                    'c7':String(),'c8':String(),'c9':String(),'c10':String(),'c11':String(),'c12':String(),
                    'c13':String(),'c14':String(),'c15':String(),'c16':String(),'c17':String(),'c18':String(),
                    'c19':String(),'c20':String(),'c21':String(),'c22':String(),'c23':String(),'c24':String(),
                    'c25':String(),'c26':String(),'c27':String(),'c28':String(),'c29':String(),'c30':String(),
                    'c31':String(),'c32':String(),'c33':String(),'c34':String(),'c35':String(),'c36':String(),
                    'c37':String(),'c38':String(),'c39':String(),'c40':String(),'c41':String(),'c42':String(),
                    'c43':String(),'c44':String(),'c45':String(),'c46':String(),'c47':String(),'c48':String(),
                    'c49':String(),'c50':String(),'c51':String(),'c52':String(),'c53':String(),'c54':String(),
                    'c55':String(),'c56':String(),'c57':String(),'c58':String(),'c59':String(),'c60':String(),
                    'c61':String(),'c62':String(),'start_date':Date(),'end_date':Date(),'location':String(),
                    'show':String()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_nums_maps(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"grid_row": Integer(),
                    'c1':Integer(),'c2':Integer(),'c3':Integer(),'c4':Integer(),'c5':Integer(),'c6':Integer(),
                    'c7':Integer(),'c8':Integer(),'c9':Integer(),'c10':Integer(),'c11':Integer(),'c12':Integer(),
                    'c13':Integer(),'c14':Integer(),'c15':Integer(),'c16':Integer(),'c17':Integer(),'c18':Integer(),
                    'c19':Integer(),'c20':Integer(),'c21':Integer(),'c22':Integer(),'c23':Integer(),'c24':Integer(),
                    'c25':Integer(),'c26':Integer(),'c27':Integer(),'c28':Integer(),'c29':Integer(),'c30':Integer(),
                    'c31':Integer(),'c32':Integer(),'c33':Integer(),'c34':Integer(),'c35':Integer(),'c36':Integer(),
                    'c37':Integer(),'c38':Integer(),'c39':Integer(),'c40':Integer(),'c41':Integer(),'c42':Integer(),
                    'c43':Integer(),'c44':Integer(),'c45':Integer(),'c46':Integer(),'c47':Integer(),'c48':Integer(),
                    'c49':Integer(),'c50':Integer(),'c51':Integer(),'c52':Integer(),'c53':Integer(),'c54':Integer(),
                    'c55':Integer(),'c56':Integer(),'c57':Integer(),'c58':Integer(),'c59':Integer(),'c60':Integer(),
                    'c61':Integer(),'c62':Integer(),'start_date':Date(),'end_date':Date(),'location':String(),
                    'show':String()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_row_maps(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"grid_row": Integer(),
                    'c1':String(),'c2':String(),'c3':String(),'c4':String(),'c5':String(),'c6':String(),
                    'c7':String(),'c8':String(),'c9':String(),'c10':String(),'c11':String(),'c12':String(),
                    'c13':String(),'c14':String(),'c15':String(),'c16':String(),'c17':String(),'c18':String(),
                    'c19':String(),'c20':String(),'c21':String(),'c22':String(),'c23':String(),'c24':String(),
                    'c25':String(),'c26':String(),'c27':String(),'c28':String(),'c29':String(),'c30':String(),
                    'c31':String(),'c32':String(),'c33':String(),'c34':String(),'c35':String(),'c36':String(),
                    'c37':String(),'c38':String(),'c39':String(),'c40':String(),'c41':String(),'c42':String(),
                    'c43':String(),'c44':String(),'c45':String(),'c46':String(),'c47':String(),'c48':String(),
                    'c49':String(),'c50':String(),'c51':String(),'c52':String(),'c53':String(),'c54':String(),
                    'c55':String(),'c56':String(),'c57':String(),'c58':String(),'c59':String(),'c60':String(),
                    'c61':String(),'c62':String(),'start_date':Date(),'end_date':Date(),'location':String(),
                    'show':String()
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()


def Inputs_search_load_status_info(showname,filename, table_name):

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
			df.to_sql(table_name,if_exists = 'replace', con=engine, schema='raw',index=False, chunksize=1000,
					dtype={"location": String(),'show':String(),'status_id':String(),'status_name':String(),
                    'status_description':String(),'start_date':Date(),'end_date':Date()
                                       
					})
			
			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)
			mail.To = "{}".format(alert_emails('12'))
			mail.Subject = "{}".format(alert_subject('12'))
			formatted_body = alert_body('12')
			mail.Body = "{}".format(formatted_body.format(show=showname, file_name=filename))
			mail.Send()
