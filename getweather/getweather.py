import pandas as pd
import json

def CityInfo():
    '''
    Introduction:
    CityInfo()function aims to return a dataset that shows the information such as city id, city, state, country, latitude, longitude of all the cities in the world.
    
    Parameters:
    No parameter.
    
    Output:
    a dataset of city id, city, state, country, latitude, longitude covering all the cities in the world
    
    '''
    from importlib import resources 
    with resources.open_binary('getweather', 'city.json') as f: 
        content = f.read()
    content1=content.decode('UTF-8')
    city=pd.DataFrame(json.loads(content1))
    
    table1=city[['id', 'name', 'state', 'country']] # extract id, name, state, state, country
    
    result2=[]  # extract lon and lat
    for i in city['coord']:
        coord={}
        coord['lon']=i.get('lon')
        coord['lat']=i.get('lat')
        result2.append(coord)
    result2
    table2=pd.DataFrame(result2)
    
    city_new=pd.concat([table1, table2], axis=1) # combine table1 and table2
    return city_new

def CityCoord(name):
    '''
    Introduction:
    This functin allows users to input the city name and then return the longitude and latitude of that city.
    
    Parameters:
    name: a city name
    
    Output:
    a tuple (lon, lat) that contains longitude and latitude of a city.
    
    Example:
    >>>CityCorrd('Taglag')
    (44.98333, 38.450001)
    '''
    city=CityInfo()
    if name in list(city['name']):
        for i in range(len(city['id'])):
            if city.iloc[i,1]==name:
                lon=city.iloc[i,4]
                lat=city.iloc[i,5]
                return lon, lat
    else:
         print("No such city! Please check your city name.")

def CityId(name):
    '''
    Introduction:
    This function allows users to input the city name and then return the city id of that city.
    
    Parameters:
    name: a city name
    
    Output:
    a city id
    
    Example:
    >>>CityId('Taglag')
    3245
    '''
    city=CityInfo()
    if name in list(city['name']):
        for i in range(len(city['name'])):
            if city.iloc[i,1]==name:
                return int(city.iloc[i,0])
    else:
        print("No such city! Please check your city name.")

def CityIds(*args):
    '''
    Introduction:
    This function allows users to input any number of city names that they want and then return the city ids of these city.
    
    Parameters:
    *args: any number of city names
    
    Output:
    a string that contains the city ids of all the cities that you input
    
    Example:
    >>>CityIds('London','Shanghai','New York')
    '2643743,1796236,5128638'
    '''
    ids=''
    for city in args:
        cityid=str(CityId(city))
        if len(ids)==0:
            ids=cityid
        else:
            ids=ids+','+cityid
    return ids

def getonecity(api_key, city_name, status='current'):
    '''
    Introduction:
    This function can return either current weather and air pollution information or the daily forecast data for 7 days.
    
    Parameters:
    api_key: your api key of the Openweather website. You can access your api key by creating an account on this website: https://home.openweathermap.org/api_keys
    city_name: one city name 
    status:status could be either 'current' or 'forecast'. If status is set to 'current', this function will return the current weather data; otherwise, it will return the forecast weather data.
    
    Output:
    If you set status to 'current', the output is dataset showing the detailed current weather information of the city you chose.
    If you set status to 'forecast', the output consists of two parts.
       The first part is a graph showing the maximum, minimum, and day temperature trends and probability of precipitation in 7 days.
       The second part is a dataset showing the detailed forecast weather information of the city you chose.
    
    '''
    if status=='current':  #get current weather data
        # Step1:run the 1st GET request to get weather information and check the status of the request
        import requests
        from requests.exceptions import HTTPError
        try:
            params1 = {'appid':api_key,'q':city_name,'units':'metric'} # 'units=metric' means temperature in Celsius and wind speed in meter/sec. 
            r1=requests.get('https://api.openweathermap.org/data/2.5/weather', params = params1)
            r1.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurrred: {err}')
        
        # Step2:parse the 1st response         
        R1 = r1.json()
        import pandas as pd
        result1=pd.DataFrame({'name':R1['name']},index=[0]) #get city name
        
        R1_sys=pd.DataFrame(R1['sys'],index=[0]) # get country name
        result2=R1_sys[['country']]
    
        R1_weather=pd.DataFrame(R1['weather']) #get weather discription
        result3=R1_weather[['description']]
       
        R1_main=pd.DataFrame(R1['main'],index=[0])  #get weather data
        result4=R1_main

        R1_wind=pd.DataFrame(R1['wind'], index=[0]) # get wind speed
        result5=R1_wind[['speed']]
   
        result6=pd.DataFrame({'visibility':R1['visibility']},index=[0]) #get visibility
        
        # Step3: run the 2nd GET request to get air pollution and check the status of the request
        ## get lon & lat
        coord=CityCoord(city_name)
        lon=coord[0]
        lat=coord[1]
        ## run the GET request and check the status of the request
        try:
            params2 = {'appid':api_key,'lat':lat,'lon':lon}
            r2 = requests.get('https://api.openweathermap.org/data/2.5/air_pollution', params = params2)
            r2.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurrred: {err}')
        
        #Step4: parse the 2nd response 
        R2 = r2.json()
        R2_list=pd.DataFrame(R2['list'])
        result7=[]
        for i in R2_list['components']:
            pollution={}
            pollution['AirPollution_co']=i.get('co')
            pollution['AirPollution_nh3']=i.get('nh3')
            pollution['AirPollution_no']=i.get('no')
            pollution['AirPollution_no2']=i.get('no2')
            pollution['AirPollution_o3']=i.get('o3')
            result7.append(pollution)
        result7=pd.DataFrame(result7)
        
        #Step5: combine the columns of result1 to result7 and return a Python object to the user of the function
        dataset1=pd.concat([result1,result2,result3,result4,result5,result6,result7], axis=1)
        dataset1.rename(columns={'speed':'wind_speed'}, inplace = True)
        return dataset1
    
    
    elif status=='forecast':  # Daily forecast for 7 days
        # Step1:run the 3rd GET request to get forecast temperature and check the status of the request
        ## get lon & lat
        coord=CityCoord(city_name)
        lon=coord[0]
        lat=coord[1]
        ## run the GET request and check the status of the request
        import requests
        from requests.exceptions import HTTPError
        try: 
            params3 = {'appid':api_key,'lat':lat,'lon':lon, 'exclude':'current,minutely,hourly','units':'metric'} # 'current,minutely,hourly' There is no whitespace between current, minutely, and hourly.
            r3 = requests.get('https://api.openweathermap.org/data/2.5/onecall', params = params3)
            r3.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurrred: {err}')
            
        #Step2: parse the 3rd response 
        import pandas as pd
        R3 = r3.json()
        R3_daily = pd.DataFrame(R3['daily'])
        R3_daily['date']=''
        ## convert timestamp to normal time
        import time
        for i in range(len(R3_daily['dt'])):
            R3_daily.iloc[i,15]=time.strftime("%Y-%m-%d",time.localtime(R3_daily.iloc[i,0]))
        
        
        R3_daily_temp=pd.DataFrame(dict(R3_daily['temp']))  # get temperature data
        R3_daily_tempT = pd.DataFrame(R3_daily_temp.values.T, index=R3_daily_temp.columns, columns=R3_daily_temp.index) # transpose R3_daily_temp
        R3_daily_tempT['date']=''  # add 'date' column
        for i in range(len(R3_daily_tempT['day'])):
            R3_daily_tempT.iloc[i,6]=R3_daily.iloc[i,15]
        
        R3_daily_pop=pd.DataFrame(R3_daily['pop']) # Probability of precipitation
        y_bar=R3_daily['pop']
        
        # Step3: concat and return a Python object to the user of the function
        dataset2=pd.concat([R3_daily_tempT,R3_daily_pop], axis=1)
        dataset2.rename(columns={'day':'day_temperature','min':'min_temperature','max':'max_temperature','night':'night_temperature','eve':'evening_temperature','morn':'morning_temperature','pop':'Probability_of_precipitation'}, inplace = True)
        dataset2.set_index(['date'], inplace=True)
        
        #Step4: draw a graph
        from matplotlib import pyplot
        import matplotlib.pyplot as plt
        
        x=dataset2.index  
        y_min=R3_daily_tempT['min']
        y_max=R3_daily_tempT['max']
        y_day=R3_daily_tempT['day']

        fig, ax1 = plt.subplots()
        ax1.plot(x, y_min, color='green', marker='o',label='minimum temperature')
        ax1.plot(x, y_max, color='red', marker='*',label='maximum temperature')
        ax1.plot(x, y_day, color='orange', marker="x",label='day temperature')
        ax1.set_xlabel('day')
        ax1.set_ylabel("temperature\u2103")
        plt.legend() # to show the label
        
        ax2 = ax1.twinx() #use same x axis with the first plot
        ax2.bar(x, y_bar,alpha=0.3)
        ax2.set_ylabel('Probability of precipitation', color='b')
        plt.title('Daily forecast for 7 days')
        # rotate the xticklabels
        for label in ax1.get_xticklabels():
            label.set_rotation(70)
        
        import os                 # automatically save picture in working directory
        path1=os.getcwd()
        path2='dailyforecast.jpg'
        path = os.path.join(path1,path2)
        plt.savefig(path) 
        plt.show()
        
        return dataset2   
    
    else:
        print('No such status. Please input either "current" or "forecast".')

def getcities(api_key, *city_name):
    '''
    Introduction:
    This is a functio aims to return current weather data for any number of cities you want.
    
    Parameters:
    api_key: your api key of the Openweather website. You can access your api key by creating an account on this website: https://home.openweathermap.org/api_keys
    *city_name: any number of city names
    
    Output:
    The first part is a bar chart showing the current temperatures of all the cities you chose.
    The second part is a dataset showing the detailed current weather information of all the cities you chose.
    
    '''
    # Step1:get city ids
    ids=CityIds(*city_name)
    
    # Step2:run the GET request and check the status of the request
    import requests
    from requests.exceptions import HTTPError
    try:
        params4 = {'appid':api_key, 'id':ids, 'units':'metric'} 
        r4 = requests.get('https://api.openweathermap.org/data/2.5/group', params = params4)
        r4.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurrred: {err}')
    
    # Step3: parse the response 
    R4 = r4.json()
    R4_list = pd.DataFrame(R4['list'])
    
    result1= R4_list['name']  # City name
    result1_df=pd.DataFrame(result1)
    
    result2=[]  # Country name
    for i in R4_list['sys']:
        country={}
        country['country']=i.get('country')
        result2.append(country)
    result2
    result2_df=pd.DataFrame(result2)
    
    result3=[]  # Temperature data
    for main in R4_list['main']:
        temperature={}
        temperature['temp']=main.get('temp')
        temperature['feels_like']=main.get('feels_like')
        temperature['humidity']=main.get('humidity')
        temperature['temp_min']=main.get('temp_min')
        temperature['temp_max']=main.get('temp_max')
        temperature['pressure']=main.get('pressure')
        result3.append(temperature)
    result3
    result3_df=pd.DataFrame(result3)
    
    result4=[]  # wind speed data
    for i in R4_list['wind']:
        wind={}
        wind['wind speed']=i.get('speed')
        result4.append(wind)
    result4
    result4_df=pd.DataFrame(result4)
    
    # Step4: combine the columns of result1 to result4 and return a Python object to the user of the function
    dataset3=pd.concat([result1_df,result2_df,result3_df,result4_df], axis=1)
    
    #Step5:draw a graph
    from matplotlib import pyplot
    import matplotlib.pyplot as plt

    x=dataset3['name']
    y=dataset3['temp']
    ylabel=[str(y1)+'\u2103' for y1 in y]
    
    plt.bar(x, y, alpha=0.3, width=0.1)
    plt.ylabel('temperature\u2103')
    for a, b, label in zip(x,y,ylabel):
        plt.text(a,b,label, ha='center', va='bottom')
    plt.title('Current Temperature')
    
    import os                 # automatically save picture in working directory
    path1=os.getcwd()
    path2='currenttemp.jpg'
    path = os.path.join(path1,path2)
    plt.savefig(path) 

    return dataset3

def getcitycircle(api_key, city_name, cnt=10):
    '''
    Introduction:
    This function aims to return weather data from cities laid within definite circle that is specified by center point(city that you input) and expected number of cities around this point.

    Parameters:
    api_key: your api key of the Openweather website. You can access your api key by creating an account on this website: https://home.openweathermap.org/api_keys
    city_name: one city name
    cnt: the number of cities around the center point. The default value is 10.
    
    Outputs:
    The output is a dataframe showing the detailed current weather information of all the cities laid withini a definite circle.
    
    '''
    #Step1: get city's lon and lat
    coord=CityCoord(city_name)
    lon=coord[0]
    lat=coord[1]
    
    #Step2: run the GET request and check the status of the request
    import requests
    from requests.exceptions import HTTPError
    try:
        params5 = {'appid':api_key,'lat':lat,'lon':lon,'cnt':cnt, 'units':'metric'}
        r5 = requests.get('https://api.openweathermap.org/data/2.5/find', params = params5)
        r5.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
        
    # Step3:parse the response and return a Python object to the user of the function
    R5 = r5.json()
    import pandas as pd
    R5_list = pd.DataFrame(R5['list'])
    
    result1= R5_list['name']  # city name
    result1_df=pd.DataFrame(result1)
    
    result2=[]   # Country name
    for i in R5_list['sys']:
        country={}
        country['country']=i.get('country')
        result2.append(country)
    result2_df=pd.DataFrame(result2)
    
    result3=[]   # Temperature data
    for i in R5_list['main']:
        temperature={}
        temperature['temp']=i.get('temp')
        temperature['feels_like']=i.get('feels_like')
        temperature['humidity']=i.get('humidity')
        temperature['temp_min']=i.get('temp_min')
        temperature['temp_max']=i.get('temp_max')
        temperature['pressure']=i.get('pressure')
        result3.append(temperature)
    result3_df=pd.DataFrame(result3)
    
    result4=[]   # wind speed data
    for i in R5_list['wind']:
        wind={}
        wind['wind speed']=i.get('speed')
        result4.append(wind)
    result4_df=pd.DataFrame(result4)
    
    weather=pd.DataFrame(dict(R5_list['weather'])) # weather description
    result5=[]
    for i in range(len(R5_list['weather'])):
        description={}
        description['description']=weather.iloc[0,i].get('description')
        result5.append(description)
    result5_df=pd.DataFrame(result5)
    
    # combine the columns of result1 to result5
    dataset=pd.concat([result1_df,result2_df,result3_df,result4_df,result5_df], axis=1)
    return dataset