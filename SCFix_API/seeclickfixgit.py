
## Manipulate the SeeClickFix API to find illegal dumping sites
## Then, post a clean-up message with a link to a community organizer website

__author__ = "miller.tim"
__date__ = "$Jan 26, 2017 6:06:40 PM$"

from watchareas import WatchArea
from cleanup import CleanUp

def main():    
    #Create an watch area for Oakaland
    watchAreaID = 35332 #Oakland Test Watch Area
    typeIssue = "Illegal Dumping"
    status = "open,acknowleged"
#    oaklandWatchArea = WatchArea(watchAreaID, typeIssue, status)
#    
##    Call for dumping sites until at least one is found. 
##    Do Not Exceed 10 pages of calls
#    maxPages = 10
#    getDumpingSites(oaklandWatchArea,maxPages)
#    
#    #Find all reporters associated with the found dumping sites
#    oaklandWatchArea.callForReporters()
#    #Display the dumping sites associated with each reporter
#    oaklandWatchArea.displayReporters()
##   Display the reporters associated with each dumping site
#    oaklandWatchArea.displayIssues()

#   Chose a dumping Site
    dumpingSite = 0
#    dumpingSites = oaklandWatchArea.getIssues()
#    for key in dumpingSites.keys():
#        dumpingSite = dumpingSites[key]
        
#   Create and post a Clean Up for the chosen dumping site
    username = ""#Requires a username and password for test.seeclickfix.com
    password = ""
    cleanup = CleanUp(dumpingSite, username, password)
#    cleanup.setData()
#    response = cleanup.share()
    #Trying to 'acknowledge' a clean up gives a 403 error
    id = 1317203
#    updateType = 2 #0 = comment, 1= open, 2 =close
#    comment = "Test: This clean-up is complete" 
#    response = cleanup.update(1317192, "close")#status can be open or closed
    updateType = 0 #comment
    comment = "Test: Someone created a cleanup" 
    response = cleanup.update(id, updateType, comment)
    print(response)
    print("end")

#Function allows the calls to cycle through more than one page
def getDumpingSites(watchArea, maxPages):
    i = 0 
    while watchArea.getNumIssues() <= 0 and i < maxPages:
        watchArea.callForIssues()
        i =+ 1  


main()
