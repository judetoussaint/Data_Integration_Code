from modules import get_conn, truncate_table_name
import pandas as pd

engine = get_conn()


def create_table_latest_marquee_prices(table_name,existing_table_1,existing_table_2):
	
	print('Creating a Table.')
	sql = '''select distinct a.* from raw."{0}" as a 
	left join raw."{1}" as b on a.evcode = b.event_code 	
	where b.show_date >= a.file_date - 2 or b.show_date is null'''.format(existing_table_1,existing_table_2) 
	
	
	df = pd.read_sql_query(sql, con=engine)
	df.to_sql(table_name,if_exists = 'replace', con=engine, chunksize=1000, schema='consumption',index=False)
	print('Temp table created')
	return df

def delete_recent_date_Marq(hist_table_name,recent_table_name):
	engine.execute(''' select * from raw."{0}" 
	where run_date =(select max(file_date) from raw."{1}")'''.format(hist_table_name,recent_table_name))
	print('it done')


def delete_recent_date_Trans(hist_table_name,recent_table_name):
	engine.execute(''' delete from raw.{0} 
	where transaction_date =(select max(transaction_date) from raw.{1})'''.format(hist_table_name,recent_table_name))
	print('it done')


def insert_recent_data_into_hist(hist_table_name,recent_table_name):
	engine.execute('''insert into raw.{0} select * from raw.{1}'''.format(hist_table_name,recent_table_name))
	print('really done')



