#! python3
#importing modules
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import requests
from datetime import datetime, date, timedelta
import subprocess
import time
import sys

#User specified inputs
age_filter = 45 #possible options = 18, 45, None
vac_name = "COVISHIELD" #possible options = "COVAXIN", "COVISHIELD", None
fee_filter = None #possible options = "Free" "Paid" None
min_slots = 5 #min available slots must be equal to or greater than min_slots for alarm to be raised
district_id = [141,145,140,146,147,143,148,149,144,150,142] #can specify multiple district ids get district id from cowin platform(see readme for more details)
hrs = 0 #number of hrs you want the program to run, cannot be None or blank, must be an whole number
mins = 15 #number of mins you want the program to run, cannot be None or blank, must be an whole number
open_browser = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #if you want to automatically open cowin sign in page if conditions are met, specify the browser path here. Else choose None

#prints input for log
print('age_filter is: ' + str(age_filter))
print('vac_name is: ' + str(vac_name))
print('fee_filter is: ' + str(fee_filter))
print('min_slots is: ' + str(min_slots))
print('district_id is: ' + str(district_id))
print('open_browser is: ' + str(open_browser))
print('hrs is: ' + str(hrs))
print('mins is: ' + str(mins)+ '\n')


#clock code - keeps time of the script run
#Takes input for hours and minutes
x = hrs
y = mins
x = int(x)
y = int(y)

#prints start time in HH:MM:SS format
start_time = datetime.now()
start = start_time.strftime('%H:%M:%S')
print("The start time is " + start)

#prints end time in HH:MM:SS format
stop_after = timedelta(hours = x, minutes = y)
end_time = start_time + stop_after
end = end_time.strftime('%H:%M:%S')
print("The end time is " + end)

#calculates time_left_script, this variable will be updated to estimate how much more time the script must run
time_left_script = (y*60) + (x*60*60)


#system inputs
today_date = datetime.today().strftime('%d-%m-%Y')
print('Fetching data for ' +str(today_date) + ' and the next 7 days' )

#Main Programme

#Max requests to the server in a 5 min time frame is restricted to 100, secs_until_newwin indicates seconds left until new window of 5 mins starts
#requests_left indicates availabel requests in seconds until new window
#The optimization for 100 requests assumes the user will be running the program for more than 5 minutes, atleast. 
#If not, the program will run only a few batches of program when more could have been run to complete the 100 request limit
secs_until_newwin = (5*60)
requests_left = 100

iteration_number = 1 #iteration means the number of times requests are sent to the server

  
while time_left_script>0:
    start_time_iteration = time.time()
    
    try:
        #1.Loops through district_id, parses request result for each element and concatenates in dataframe 
        #2.Applies filters and generates final dataframe
        print('iteration number: '+str(iteration_number))
        
        df = pd.DataFrame()
        for i in district_id:
            iteration_number+=1
            URL = r"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(i,today_date)
            #The user-agent line helps identify the browser and operating system of the user(who generates the request)
            pi = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
            request_response = requests.get(URL, headers = pi)
            dict_req_resp = request_response.json()
            
            for key,value in (dict_req_resp.items()):
                for element in range(len(value)):
                    for i,j in value[element].items():
                        df_iteration = pd.DataFrame.from_dict(value[element])
                        df = pd.concat([df,df_iteration])
        
        if df.empty:
            print('No records found for this iteration')
    
        else:
            #Applying filters
            df_fin = df[(df['available_capacity']>=min_slots)]
            ##vaccine filter
            if vac_name is not None:
                df_fin = df_fin[df_fin['vaccine']==vac_name]
                
            #age limit filter
            if age_filter is not None:
                df_fin = df_fin[df_fin['min_age_limit']==age_filter]
                
            #fee filter
            if fee_filter is not None:
                df_fin = df_fin[df_fin['fee_type']==fee_filter]
            
            df_fin.reset_index(inplace = True)
            df_fin.drop(columns={'index'},inplace = True)
            
            #opens alarm, prints df_fin and launches webpage
            if len(df_fin)>0:
                subprocess.Popen(['start','success_song.mp3'], shell = True)
                print(df_fin)
                if opne_browser is not None:
                    subprocess.Popen([open_browser, r"https://selfregistration.cowin.gov.in/"])
            
             
        
    except:
        print('Number of requests exceeded')
    
    end_time_iteration = time.time()
    #sleep_time calculates how long we should let the program sleep so that 100 requests can be made in 5 minute window
    sleep_time = ((secs_until_newwin*len(district_id))/requests_left)-(end_time_iteration-start_time_iteration)
    print('time_taken to run the batch: ' +str(end_time_iteration-start_time_iteration) + ' seconds') #here, batch means the entire group of district id.
    print('sleep time: '+str(sleep_time)+ ' seconds')
    secs_until_newwin = secs_until_newwin - sleep_time
    requests_left = requests_left - len(district_id)
    print('updated secs_until_newwin is ' + str(secs_until_newwin))
    print('updated requests_left is ' + str(requests_left)+'\n')
    time_left_script = time_left_script-(end_time_iteration-start_time_iteration)-sleep_time
    time.sleep(sleep_time)
    
    if sleep_time>secs_until_newwin:
        secs_until_newwin = (5*60)
        requests_left = 100
