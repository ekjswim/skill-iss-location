## Python program to test using open-notify.org & geonames.org
## I run this on the command line with an ISS tracking web site
## such as http://www.isstracker.com/ open to compare results
## the ISS is moving fast, so lat & lng results may be slightly off
## works so far in Python2.7

import urllib2
import json

# get the 'current' latitude and longitude of the ISS from open-notify.org in JSON
reqISSLocation = urllib2.Request("http://api.open-notify.org/iss-now.json")
resISSLocation = urllib2.urlopen(reqISSLocation)
issObj = json.loads(resISSLocation.read()) # JSON payload of ISS location data
latISS = issObj['iss_position']['latitude']
lngISS = issObj['iss_position']['longitude']

# construct a string witj ISS lat & long to determine a geographic object/toponym associated with it
# This is "Reverse Gecoding" availbe from geonames.org
# Sign up for a free user name at http://www.geonames.org/ and repalce YourUserName with it
# !! remember to activate web servoces for your user name !!
oceanGeoNamesReq    = "http://api.geonames.org/oceanJSON?lat="+ latISS +"&lng="+ lngISS +"&username=YourUserName"
landGeoNamesReq     = "http://api.geonames.org/countryCodeJSON?formatted=true&lat=" + latISS + "&lng=" + lngISS +"&username=YourUserName&style=full"


# Since the Earth is 3/4 water, we'll chek to see if the ISS is over water first;
# in the case where this is not so, we handle the exception by  searching for a country it is
# over, and is this is not coded for on GenNames, we just we say we don't know

oceanGeoNamesRes = urllib2.urlopen(oceanGeoNamesReq)
toponymObj = json.loads(oceanGeoNamesRes.read())
try:
    toponym = toponymObj['ocean']['name']
except KeyError:
    landGeoNamesRes = urllib2.urlopen(landGeoNamesReq)
    toponymObj = json.loads(landGeoNamesRes.read())
    toponym = toponymObj['countryName']
except:
    toponym = "unknown"

print "the ISS is over: " + toponym
