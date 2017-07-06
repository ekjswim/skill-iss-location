# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

import urllib2 # need for api-open-notify
import json    # need for api-open-notify

from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'GregV', '@lachendeKatze'

class ISSLocationSkill(MycroftSkill):
    def __init__(self):
        super(ISSLocationSkill, self).__init__(name="ISSLocationSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))
        
        iss_location_intent = IntentBuilder("ISSLocationIntent").require("ISSKeyword").build()
        self.register_intent(iss_location_intent, self.handle_intent)

    def handle_intent(self, message):
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
        oceanGeoNamesReq = "http://api.geonames.org/oceanJSON?lat="+ latISS +"&lng="+ lngISS +"&username=YourUserName"
        landGeoNamesReq  = "http://api.geonames.org/countryCodeJSON?formatted=true&lat=" + latISS + "&lng=" + lngISS +"&username=YourUserName&style=full"

        # Since the Earth is 3/4 water, we'll chek to see if the ISS is over water first;
        # in the case where this is not so, we handle the exception by  searching for a country it is
        # over, and is this is not coded for on GenNames, we just we say we don't know

        oceanGeoNamesRes = urllib2.urlopen(oceanGeoNamesReq)
        toponymObj = json.loads(oceanGeoNamesRes.read())
        try:
            toponym = "the " + toponymObj['ocean']['name']
        except KeyError:
            landGeoNamesRes = urllib2.urlopen(landGeoNamesReq)
            toponymObj = json.loads(landGeoNamesRes.read())
            toponym = toponymObj['countryName']
        except:
            toponym = "unknown"

        # print "the ISS is over: " + toponym
        if toponym == "unknown":
            self.speak_dialog("location.unknown",{"latitude": latISS, "longitude": lngISS})
        else:
            self.speak_dialog("location.current",{"latitude": latISS, "longitude": lngISS, "toponym": toponym})

    def stop(self):
        pass

def create_skill():
    return ISSLocationSkill()
