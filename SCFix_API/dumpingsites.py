#Manage Dumping Sites in the Watch Area

__author__ = "miller.tim"
__date__ = "$Feb 17, 2017 9:38:02 AM$"

class DumpingSite(object):
        
        def __init__(self, ident, summary, status, lat, lng, address):
            self.ident = ident
            self.summary = summary
            self.status = status
            self.lat = lat
            self.lng = lng
            self.address = address
            self.reporters = [] #Only holds the reporter id, not the whole object

        ##Modification Functions
        def addReporter(self, newReporter):
            self.reporters.append(newReporter)
        
        def closeSite(self):
            self.status = "closed"
            
        def acknowledgeSite(self):
            self.status = "acknowledged"
            
        def openSite(self):
            self.status = "open"
            
        ##Retrieval Functions
        def getIdent(self):
            return(self.ident)

        def getSummary(self):
            return(self.summary)
        
        def getStatus(self):
            return (self.status)

        def getLat(self):
            return(self.lat)

        def getLng(self):
            return(self.lng)
        
        def getAddress(self):
            return(self.address)

        def getReporters(self):
            return(self.reporters)

        def getOneReporter(self):
  return(self.reporters[0])
