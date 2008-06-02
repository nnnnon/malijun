import base64, httplib, urllib

class TwitterAPI:
    def __init__(self, username, password):
        # generate authentication header string
        self.authentication = { "Authorization": "Basic %s"
            % base64.encodestring("%s:%s" % (username, password)).strip() }

        # create connection
        self.connection = httplib.HTTPConnection("twitter.com", 80)

    def update_status(self, status):
        # send post response with authenticated status
        self.connection.request("POST", "/statuses/update.xml",
            urllib.urlencode({ "status": status }), self.authentication)
        response = self.connection.getresponse()
        return response.status
