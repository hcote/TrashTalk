##Organize meetups for illegal dump sites

__author__ = "miller.tim"
__date__ = "$Feb 17, 2017 9:50:13 AM$"

import requests
import json


class CleanUp(object):

        def __init__(self, dumpingSite, username, password):
            self.dumpingSite = dumpingSite
            self.data = {}
            self.description = "Clean up dumping Site (id: %s) at: trashtalk.com"
            self.username = username
            self.password = password
            self.header = {"Content-type": "application/json"}
            self.baseCallRequest = "https://test.seeclickfix.com/api/v2/issues"
            

        def setData(self):
            self.payload={
                "lat":self.dumpingSite.getLat(),
                "lng":self.dumpingSite.getLng(),
                "address":self.dumpingSite.getAddress(),
                "request_type_id":"other",
                "answers":{
                    "summary":"Meet-Up to Clean-Up",
                    "description": "Test: " + self.description % self.dumpingSite.getIdent()
                }
            }
        
        def share(self):
            api_request = requests.post(self.baseCallRequest, auth = (self.username, self.password), data = json.dumps(self.payload), headers = self.header)#Currently Posts to the test site
            return api_request
        
        def update(self, id, choice, comment):#choice allows either a change of status or simple post of comment
            options = ["comments", "open", "close"]
            url = self.baseCallRequest + "/%s/%s" % (id, options[choice])
            comment = json.dumps({"comment":comment})#changing a status  requires a comment
            api_request = requests.post(url, auth = (self.username, self.password), data = comment, headers = self.header )
return api_request
