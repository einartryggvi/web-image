#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib2
from bs4 import BeautifulSoup
import urlparse

class GMT(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=10) # + self.dst(dt)
    def tzname(self, dt):
        return "GMT"
    def dst(self, dt):
        return datetime.timedelta(0) 
 
class Util(object):
     
    def get_expiration_stamp(self,seconds):
        gmt = GMT() 
        delta = datetime.timedelta(seconds=seconds)
        expiration = self.get_current_time()
        expiration = expiration.replace(tzinfo=gmt) 
        expiration = expiration + delta
        EXPIRATION_MASK = "%a, %d %b %Y %H:%M:%S %Z"
        return expiration.strftime(EXPIRATION_MASK)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'image/png'
	self.response.headers["Expires"] = util.get_expiration_stamp(7 * 86400)
	self.response.headers["Cache-Control: max-age"] = 7 * 86400
	self.response.headers["Cache-Control"] = "public"
        url = self.request.get('url')
        domain = urlparse.urlparse(url)
        domain = domain.scheme + '://' + domain.hostname + '/'
        try:
            html = BeautifulSoup(urllib2.urlopen(url).read())
            apple = html.find('link', {'rel': 'apple-touch-icon'})
            favicon = html.find('link', {'rel': 'icon'})
            facebook = html.find('meta', {'property': 'og:image'})
            if apple:
                href = apple['href']
                if 'http' not in apple['href']:
                    href = domain + apple['href']
                self.response.write(urllib2.urlopen(href).read())
            elif facebook:
                href = facebook['content']
                if 'http' not in facebook['content']:
                    href = domain + facebook['content']
                self.response.write(urllib2.urlopen(href).read())
            elif favicon:
                href = favicon['href']
                if 'http' not in favicon['href']:
                    href = domain + favicon['href']
                self.response.write(urllib2.urlopen(href).read())
            else:
                self.response.write(urllib2.urlopen(domain + '/favicon.ico').read())
        except Exception as e:
            self.response.write(open('./icon.png').read())


app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
