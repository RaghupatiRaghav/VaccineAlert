# Vaccine Alert

## About 
This is a program written in Python3 to alert the user of vaccine slots available on the [Co-Win portal](https://www.cowin.gov.in/home). In a nutshell, it pings (or asks) the portal for slot information. If the retrieved information is relevant for the user (i.e., slots for a particular vaccine are available as per user's requirements), the program raises a sound alarm and opens up the login page to instantly book the slots. 

## Getting Started:

### Downloading Script:

1. Clone the repository or directly download files *final_script.py* and *success_song.mp3*.
2. Edit the python script using any text editor (such as Notepad). Navigate to ```#User specified inputs section``` in the beginning of the program.
3. Provide the following inputs:

  3. ```age_filter``` : Possible options are ```18``` and ```45```. This instructs the program to search for 18-45 and 45+ category respectively.

  * ```vac_name``` : Possible options are ```"COVAXIN"``` where the search is for Covaxin slots, ```"COVISHIELD"``` where the search is for Covishield slots and None where the search is vaccine agnostic.

  * ```fee_filter``` : Possible options are ```"Free"``` where the program searches for Free slots ```"Paid"``` where it searches for slots that are paid and ```None``` where the search is fee agnostic.

  * ```min_slots``` : Often, it will not be worth your time to look at the portal if the available slots are abysmally low. This is because such slots tend to fill up very fast when available. You may provide any integer or ```None``` here. The alarm will be raised if minimum available slots are greater than or equal to the specified integer. If ```None``` is specified, however, this filter does not apply.

  * ```district_id``` : You can provide any number of District IDs enclosed in a square bracket. For instance, ```district_id = [141,145,140,146,147,143,148,149,144,150,142]``` will search for all the specified IDs. The aforementioned list of district_id covers all of Delhi. Please visit the [Co-Win portal](https://www.cowin.gov.in/home) if you wish to alter this list for your region.

  * ```hrs``` : Specify the number of hours you want the search to run.

  * ```mins``` : Specify the number of minutes you want the search to run.

  * ```open_browser``` : Specify the program path for your browser. If ```None``` is specified, the program does not open the login page of the Cowin Portal when all conditions are met.

4. Save the script, drag and drop it into a python environment (such as Anaconda Terminal or Bash). 
5. The program will now run for and will stop either if it finds a matching slot or it exhausts the specified duration of the run.
6. To stop the script prematurely, simply press *Ctrl* and *c* simultaneously. 

*Note-1* : A *final_program.ipynb* file can also be found in this repository which allows the user to run the same program on Jupyter Notebook/Jupyter Lab. The user defined inputs remain same as above. 

*Note-2* : Government capped the maximum number of pings to CoWin servers to 100 in 5 minutes. The program is therefore optimized to space 100 requests in 5 minutes, depending on the frequency of pings. For instance, if the requests are sent at such a pace that 100 pings will be exhausted in the next 5 minutes, the wait time between these requests increases and vice versa for low pace of requests.   


### Changing alarm sound:

1. After cloning the repository or directly downloading the files, delete the existing file named _'success_song.mp3'_.
2. Copy paste preferred mp3 file in the same directory as the script *final_script.py*.
3. Rename the mp3 file to _'success_song.mp3'_.   


