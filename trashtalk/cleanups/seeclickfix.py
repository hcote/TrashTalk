import json
import requests

from django.conf import settings

# Variables for API call to test.seeclickfix.com (the developer's page)
# developer page has own set of user accounts
# Switching to live page requires removing 'test' from url and creating account for live page
HEADER = settings.SCF_HEADER
BASE_CALL = settings.SCF_BASE_CALL
ADMIN_USERNAME = settings.SCF_ADMIN_USER
ADMIN_PASSWORD = settings.SCF_ADMIN_PASSWORD
CLEANUP_BASE_URL = settings.SCF_CLEANUP_BASE_URL


# Create an initial post to SeeClickFix.com
# Requires first finding the address from geopy
# TODO: Refactor name.
def postSCFix(cleanup):
    """
    Send to SCF.

    :param cleanup:
    :return:
    """
    description = str("%s, %s: %s%s" % (cleanup.description, cleanup.event_start,
                                        CLEANUP_BASE_URL, cleanup.id))
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
    """
    Send update to SCF.
    
    :param cleanup_status:
    :param cleanup_id:
    :return:
    """
    phrase = "Test: This clean-up is actually complete"
    comment = json.dumps({"comment": phrase})
    url = BASE_CALL + "/%s/%s" % (cleanup_id, cleanup_status)

    return requests.post(url, auth=(ADMIN_USERNAME, ADMIN_PASSWORD), data=comment, headers=HEADER)
