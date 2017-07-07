#Sheets API Requires a Google Cloud services account.
#Instructions are found in this link
#http://gspread.readthedocs.io/en/latest/oauth2.html

import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds'] #Sheet must be shared with Cloud account in order to find it
validation ="" #Validation pulls from JSON account information file 
sheet_key = "" #Key from sheet URL
top_row = 2 #First Row is header #Limited ability to find the end of the data. Easier just to put data at the top and find it later

credentials = ServiceAccountCredentials.from_json_keyfile_name(validation, scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_key(sheet_key).sheet1

#Function used in cleanups.py for send_to_pw.html
def send_to_sheet(data):
    #Rough draft of data
    #TODO: Match data format of Public Works
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    data.insert(0,timestamp)
    print(data)
    wks.insert_row(data,index=top_row)
