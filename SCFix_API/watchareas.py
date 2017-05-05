
#Manage Watch Areas
#Extract issues associated with a Watch Area (Manange with Hashtable/Dict)
#Extract the Reporters associated with the issues of a Watch Area (Manage with Hashtable/Dict)

__author__ = "miller.tim"
__date__ = "$Feb 17, 2017 9:33:11 AM$"

import requests
from dumpingsites import DumpingSite
from reporters import Reporters

class WatchArea(object):        

        def __init__(self, area, typeIssue, status):
            self.baseCallIssue = "https://test.seeclickfix.com/api/v2/issues?page=%d&watcher_token=%d&search=%s&status=%s"
            self.baseCallReporter = "https://test.seeclickfix.com/api/v2/users?lat=%f&lng=%f"
            self.area = area
            self.typeIssue = typeIssue
            self.status = status
            self.allIssues = dict()
            self.allReporters = dict()
            self.page = 1
            
                
        #Add new dumping sites to hashtable
        def callForIssues(self):
            callWatchArea = requests.get(self.baseCallIssue % (self.page, self.area, self.typeIssue, self.status))
            watchArea = callWatchArea.json()
            for issue in watchArea['issues']:
                summary = issue['summary']
                ident = issue['id']
                status = issue['status']
                lat = issue['lat']
                lng = issue['lng']
                address = issue['address']
                dSite = DumpingSite(ident, status, summary, lat, lng, address)
                self.allIssues[ident] = dSite
            self.page = watchArea['metadata']['pagination']['next_page']

        #Add new reporters to hashtable
        def callForReporters(self):
            #Cycle through all of the issues
            for key in self.allIssues.keys():
                #Call the API and get the reporters for each issue. Calls are based on the GPS Coordinates of the dumping site
                issue = self.allIssues[key]
                lat = issue.getLat()
                lng = issue.getLng()
                ident = issue.getIdent()
                callReporters = requests.get(self.baseCallReporter % (lat, lng))
                reporters = callReporters.json()
                #Cycle through each reporter
                reporter = reporters['users']
                for each in reporter:                                
                    eachID = each['id']
                    eachName = each['name']
                    #Add its ID to the dumping site's keychain of reporters
                    issue.addReporter(eachID)
                    #Check whether the key for the reporter is already in the list of keys in the Reporter Hashtable
                    if eachID in self.allReporters:
                        #If the reporter is already in the Hashtable, simply add the dumping site ID to its keychain of dumping sites
                        changeReporter = self.allReporters[eachID]
                        changeReporter.addDumpingSite(ident)                                       
                    #Else, create a new reporter with the site ID on its chain, add it to the allReporters Hashtable 
                    else:
                        newReporter = Reporters(eachID, eachName, ident)
                        self.allReporters[eachID] = newReporter
        
        def getNumIssues(self):
                return (len(self.allIssues))
        
        def getIssues(self):
                return (self.allIssues)

        def getReporters(self):
                return (self.allReporters)
        
        def displayIssues(self):
            for key in self.allIssues.keys():
                singleSite = self.allIssues[key]
                #print ("Identity: %s, Summary: %s, Lat: %s, Long: %s" % (key, singleSite.getSummary(), singleSite.getLat(), singleSite.getLng()))
                print ("Summary: %s, Status: %s, A Reporter: %s" % (singleSite.getSummary(), singleSite.getStatus(), singleSite.getOneReporter()))        

        def displayReporters(self):
            for key in self.allReporters.keys():
                singleReporter = self.allReporters[key]
                print("Name: %s, A Dumping Site: %s" % (singleReporter.getName(), singleReporter.getOneDumpingSite()))
