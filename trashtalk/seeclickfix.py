import json

import requests
from input_handling import twelve_hour_time

# Variables for API call to test.seeclickfix.com (the developer's page)
# developer page has own set of user accounts
# Switching to live page requires removing 'test' from url and creating account for live page
HEADER = {"Content-type": "application/json"}
BASE_CALL = "https://test.seeclickfix.com/api/v2/issues"


# Create an initial post to SeeClickFix.com
# Requires first finding the address from geopy
def postSCFix(cleanup):
    # location = Cleanup object
    start_time = twelve_hour_time(cleanup.start_time)
    description = str("%s, %s: %s%s" % (cleanup.description, start_time, CLEANUP_BASE_URL, cleanup.id))
    payload = {
        "lat": str(cleanup.location.latitude),
        "lng": str(cleanup.location.longitude),
        "address": str(cleanup.location.number),
        "request_type": "other",
        "answers": {
            "summary": str(cleanup.name),
            "description": description
        }
    }
    # Make post to SeeClickFix
    return requests.post(BASE_CALL, auth=(ADMIN_USERNAME, ADMIN_PASSWORD), data=json.dumps(payload), headers=HEADER)


# Updating the status to opened or closed. Requires a comment with update
# The website never references this function
def updateSCFix(cleanup_status, cleanup_id):
    phrase = "Test: This clean-up is actually complete"
    comment = json.dumps({"comment": phrase})
    url = BASE_CALL + "/%s/%s" % (cleanup_id, cleanup_status)

    return requests.post(url, auth=(ADMIN_USERNAME, ADMIN_PASSWORD), data=comment, headers=HEADER)
