import urllib2
import time


update_url = "http://twitter.com/statuses/update.xml"


auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password(
    'Twitter API', 'http://twitter.com/',
    'nnnnon', '2Akgyv2a')
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)




def update(text):
    req = urllib2.Request(update_url)
    req.add_data("status="+text)
    urllib2.urlopen(req)


