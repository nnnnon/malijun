#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Shout(db.Model):
    message = db.TextProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    who = db.StringProperty()

class MyHandler(webapp.RequestHandler):
    def get(self):
        shouts = db.GqlQuery('select * from Shout '
        'order by when desc')
        values = {
          'shouts':shouts
        }
        self.response.out.write(
          template.render('main.html',
                              values))
    def post(self):
        shout = Shout(message=self.request.get('message'),
                      who = self.request.get('who'))
        shout.put()
        self.redirect('/')
def main():
    app = webapp.WSGIApplication([
    (r'.*',MyHandler)],debug=True)
    wsgiref.handlers.CGIHandler().run(app)
    
if __name__ == '__main__':
    main()