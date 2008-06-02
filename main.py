#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import datetime

from twitter import update

class Shout(db.Model):
    message = db.TextProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    #who = db.StringProperty()
    author = db.UserProperty()   
    def modify_time(self):
        return (self.when + datetime.timedelta(hours=8))\
                    .strftime("%Y年%m月%d日 %H:%M:%S")

class MyHandler(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'        
        shouts = db.GqlQuery('select * from Shout '
        'order by when desc')
        #post_time = modify_time(datetime.datetime.now())
        values = {
          'shouts':shouts,
          'url': url,
          'url_linktext': url_linktext, 
          #'post_time': post_time       
        }
        self.response.out.write(template.render('main.html',
                              values))

    def post(self):
        
        shout = Shout(message=self.request.get('message'))
        if users.get_current_user():
            shout.author = users.get_current_user()
        shout.put()
        self.redirect('/')
def main():
    
    app = webapp.WSGIApplication([
    (r'.*',MyHandler)],debug=True)
    wsgiref.handlers.CGIHandler().run(app)

def modify_time(when):
    return when + datetime.timedelta(hours=8)
if __name__ == '__main__':
    #update('hello')
    main()