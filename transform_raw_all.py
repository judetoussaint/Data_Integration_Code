import re
import pandas as pd
import pandas as np
# from sqlalchemy import create_engine,Integer, String, Date,Time


def transform_raw(filename):

    with open(filename) as file_object:
        contents = file_object.read().replace('\n',';')
    regex = r'TICKETMASTER.+?\bSEATS\b'
    important_list = re.findall(regex,contents)
    
    second_data_loop = pd.DataFrame()
    for i in range(len(important_list)):
    
        imp_list = important_list[i].split(';')
        evcode = pd.Series([imp_list[0][31:40]])
        date = pd.Series([imp_list[0][51:61].strip()])
        time = pd.Series([imp_list[0][63:68]])
        PL = pd.Series(imp_list[8].split()[1:-2])
        first_data_loop = pd.DataFrame()
        for j in range(9,len(imp_list)-2):
        #remember here imp_list is important_list[0]
            Price = pd.Series(imp_list[j].split()[1:])
            Level = pd.Series(imp_list[j].split()[0])
            data =  pd.concat([evcode, date,time,PL,Level,Price], axis=1).fillna(method='ffill')
            first_data_loop = first_data_loop.append(data, ignore_index=True)
        second_data_loop = second_data_loop.append(first_data_loop, ignore_index=True)
    second_data_loop.columns = ['evcode','date','time','PL','Level','Price']
    second_data_loop['Price'] = pd.to_numeric(second_data_loop['Price'], errors='coerce')

    return second_data_loop

