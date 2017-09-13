'''
Software stuff you need: Python 2.7, Selenium, Chrome
'''
##########
#IMPORTS
##########

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import datetime

##########
#VARIABLES
##########
''''''''''''''''''
'''INSTRUCTIONS'''
''''''''''''''''''
#Go to the timecard thing and navigate to where it tells you to log on
#Copy and paste that URL into CLASSURL
#Next, you need to find your chrome profile. Not sure if this
#is entirely necessary, but it's how I ran a previous program
#and it still works just dandy for me.
#SO: Open your file explorer, navigate to C:\Users\[your username]\AppData\Local\Google\Chrome\User\UserData
#and somewhere in there you should be able to find your Chrome Profile location. Then,
#copy that directory address to CHROMEPROFILE, while keeping the "user-data-dir=" prefix.
#Then, put your username and password in the appropriate spots.
#To run this program, save it to a folder somewhere, preferably with a .pyw extension. Then, open command prompt
#and navigate to that folder. Run the program with "python [whatever-you-named-it].pyw"
#After a second or two, the input fields will come up and you can enter your info WITH QUOTES AROUND THEM.
#E.G. "monday" [enter] "9:30AM" [enter] "4:30PM" [enter]
''''''''''''''''''
''''''''''''''''''
''''''''''''''''''
CLASSURL = "[your-url-here]"
CHROMEPROFILE = "user-data-dir=C:\[path]"
USERNAME = "[your-username]"
PASSWORD = "[your-password]"
#Leave this stuff alone. It just gives you the input message in command prompt where
#you can put in your data.
DAYWORKED1 = input("WITH QUOTES! Day Worked: ")
TIMEIN1 = input("WITH QUOTES! Time In: ")
TIMEOUT1 = input("WITH QUOTES! Time Out: ")
#Also leave alone. Just converts your data to strings.
DAYWORKED = str(DAYWORKED1)
TIMEIN = str(TIMEIN1)
TIMEOUT = str(TIMEOUT1)
#Loads your ChromeProfile so you don't open up a completely blank Chrome window
options = webdriver.ChromeOptions() 
options.add_argument(CHROMEPROFILE) #Path to your chrome profile
browser = webdriver.Chrome(chrome_options=options)


##########
#FUNCTIONS
##########
'''
NOTE: 1,3,5,7,9,11,13 are the VARS for first week. 15,17,19,21,23,25,27 are the VARS for week 2.
'''

def login(USERNAME, PASSWORD, CLASSURL):
	#Open the selected URL
	browser.get(CLASSURL) 
	time.sleep(1)
	#Find the boxes to type in the username and psk
	username = browser.find_element_by_id("USER_NAME")
	password = browser.find_element_by_id("CURR_PWD")
	#Type the stuff
	username.send_keys(USERNAME)
	password.send_keys(PASSWORD)
	#Hit enter because apparently finding the "submit" button is
	#too hard for this library
	ActionChains(browser) \
		.key_down(Keys.ENTER) \
		.key_up(Keys.ENTER) \
		.perform()
	time.sleep(1)

def timecardselect():
	#finds the first timecard checkbox
	timecardselect = browser.find_element_by_name("LIST.VAR1_1")
	#and clicks it
	timecardselect.click()
	#Clicks submit to open the card
	submitbutton = browser.find_element_by_name("SUBMIT2")
	submitbutton.click()

def THEDAY(DAYWORKED):
	#Makes the variable rowvar global so it can be referenced outside the function
	global rowvar
	#Bunch of ifs and elifs to choose the correct row for the given day of the week
	if DAYWORKED == "Sunday" or DAYWORKED == "sunday":
		rowvar = 1
	elif DAYWORKED == "Monday" or DAYWORKED == "monday":
		rowvar = 3
	elif DAYWORKED == "Tuesday" or DAYWORKED == "tuesday":
		rowvar = 5
	elif DAYWORKED == "Wednesday" or DAYWORKED == "wednesday":
		rowvar = 7
	elif DAYWORKED =="Thursday" or DAYWORKED == "thursday":
		rowvar = 9
	elif DAYWORKED == "Friday" or DAYWORKED == "friday":
		rowvar = 11
	elif DAYWORKED == "Saturday" or DAYWORKED == "saturday":
		rowvar = 13

def inthetable(TIMEIN, TIMEOUT, rowvar):
	#Turns rowvar into a string so it can be concatenated with the
	#time-in and time-out column names
	rowvarstr = str(rowvar)
	#takes the info and creates the proper html element name for Selenium
	#to look for
	timeinstr = "LIST_VAR4_" + rowvarstr
	timeoutstr = "LIST_VAR5_" + rowvarstr
	#Looks for the element
	timeinelement = browser.find_element_by_id(timeinstr)
	timeoutelement = browser.find_element_by_id(timeoutstr)
	#Enters in the time in and time out info from the user
	timeinelement.send_keys(TIMEIN)
	timeoutelement.send_keys(TIMEOUT)
	#finds the submit button and clicks it
	submitbutton = browser.find_element_by_name("SUBMIT2")
	#Pause for a few seconds to give you time to check what it entered,
	#in case there was a mistake
	time.sleep()
	submitbutton.click()
	time.sleep(1)
	okbutton = browser.find_element_by_name("OK2")
	okbutton.click()
	time.sleep(1)

##########
#CALLS
##########
#Calls the functions, with some sleep-pauses in between
#to make sure pages have time to load
login(USERNAME, PASSWORD, CLASSURL)
timecardselect()
THEDAY(DAYWORKED)
inthetable(TIMEIN, TIMEOUT, rowvar)
#Shut 'er down.
browser.quit()
