
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime

def get_tide_data():
    today_date = datetime.datetime.now().day
    today_month = datetime.datetime.now().month
    today_year = datetime.datetime.now().year
    
    
    r = requests.get("http://www.tides.gc.ca/eng/station?type=1&date="+str(today_year)+"%2F"+str(today_month)+"%2F"+str(today_date)+"&sid=990&tz=NDT&pres=1")
    data = r.text
    soup = bs(data, "html.parser")
    
    tide_data = []
    
    for x in soup.find_all('tr'):
        entry_data = []
        for y in x.find_all('td'):
            entry_data.append(y.text)
        if len(entry_data)==3:
            tide_data.append(entry_data)
    
    tide_df = pd.DataFrame(tide_data, columns=['Date', 'Time', 'Height'])
    tide_df[['Date', 'Time']]= tide_df[['Date', 'Time']].astype(str)
    tide_df['date_time']= tide_df.Date+ " " +tide_df.Time+":00"
    tide_df['date_time']= pd.to_datetime(tide_df['date_time'])
    tide_df['Height']= (tide_df['Height'].convert_objects(convert_numeric=True))
    final_data = tide_df[['date_time','Height']]
    final_data.to_csv('tide_data.csv')

