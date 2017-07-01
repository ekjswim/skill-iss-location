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
        iss_location_intent = IntentBuilder("ISSLocationIntent").require("ISSKeyword").build()
        self.register_intent(iss_loction_intent, self.handle_intent)

    def handle_intent(self, message):
        self.speak.dialog("in the space station skill intent handler")
        req = urllib2.Request("http://api.open-notify.org/iss-now.json")
        response = urllib2.urlopen(req)

        obj = json.loads(response.read())

        print obj['timestamp']
        print obj['iss_position']['latitude'], obj['iss_position']['longitude'] # fixed this line from the original code

        issLatitude =  obj['iss_position']['latitude']
        issLongitude = obj['iss_position']['longitude']

        self.speak_dialog("location.current",{"latitude": issLatitude, "longitude": issLongitude})

    def stop(self):
        pass

def create_skill():
    return ISSLocationSkill()
