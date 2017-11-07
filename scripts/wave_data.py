import pandas as pd
from datetime import datetime, timedelta


def get_wave_data():
    now = datetime.now()
    (startDate, endDate) = (now-timedelta(days = 1), now-timedelta(days = 0))
    
    url = 'http://www.smartatlantic.ca/Home/doNewRequest.php?sel=timestamp%2Clat%2Clon%2Cwave_ht_max%2Cwave_ht_sig%2Cwave_period_max%2C&db=smb_bonavista&title=Bonavista&user=a%20a&email=test%40test.de&start='+str(startDate.strftime("%Y-%m-%d"))+'&end='+str(endDate.strftime("%Y-%m-%d"))
    wave_data = pd.read_csv(url)
    wave_data['Date & Time(UTC)'] = pd.to_datetime(wave_data['Date & Time(UTC)'])
    wave_data.columns = ['date_time', 'latitude', 'longitude', 'max_wave_height', 'sig_wave_height', 'peak_wave_period']
    wave_data.tail(1).to_csv('wave_status.csv')
    