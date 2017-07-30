
__author__ = "miller.tim"
__date__ = "$Apr 1, 2017 7:52:39 PM$"

import requests
import json

# Variables for API call to test.seeclickfix.com (the developer's page)
# developer page has own set of user accounts
# Switching to live page requires removing 'test' from url and creating account for live page
ADMIN_USERNAME = "" # SeeClickFix Username and password
ADMIN_PASSWORD=''
HEADER = {"Content-type": "application/json"}
BASE_CALL = "https://test.seeclickfix.com/api/v2/issues"


# Create an initial post to SeeClickFix.com
# Requires first finding the address from geopy
def postSCFix(location):
    # location = Cleanup object
    payload = {
        "lat":str(location.lat),
        "lng":str(location.long),
        "address":str(location.address),
        "request_type":"other",
        "answers":{
            "summary":"Meet-Up to Clean-Up",
            "description":"Test of trashtalk"
        }        
    }
    # Make post to SeeClickFix
    return requests.post(BASE_CALL, auth=(ADMIN_USERNAME, ADMIN_PASSWORD), data=json.dumps(payload), headers=HEADER)


# Updating the status to opened or closed. Requires a comment with update
# The website never references this function
def updateSCFix(cleanup_status, cleanup_id):    
    phrase = "Test: This clean-up is actually complete"
    comment = json.dumps({"comment":phrase})
    url = BASE_CALL + "/%s/%s" % (cleanup_id, cleanup_status)
    
    return requests.post(url, auth=(ADMIN_USERNAME, ADMIN_PASSWORD), data=comment, headers=HEADER )
