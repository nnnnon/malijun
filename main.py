#!/usr/bin/env python
# -*- coding: utf-8 -*-
#加一个注释
import os 
import sys
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import datetime
from google.appengine.api import images
from google.appengine.api import mail
from twitter import update
from models import Shout


class MyHandler(webapp.RequestHandler):
    def get(self):
        size = 10
        currpage = self.request.get('p')
        if currpage == '':
          currpage = '1'
        page = int(currpage)
        offset = (page-1)*size
                
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = '登出'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = '登录'        
        shouts = db.GqlQuery('select * from Shout '
        'order by when desc ')
        
        nums =  shouts.count()
        
        pagestr = ''
        if page == 1 :
          if nums > size :
            pagestr = '<a href="/?p=' + str(page+1) + '">Next</a>'
          else :
            pagestr = '1'
        else :
          pagestr = '<a href="/?p='+str(page-1)+'">Pre</a>'
          if nums > size*page :
            pagestr += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + ' <a href="/?p=' + str(page+1) + '">Next</a>'
        
        #post_time = modify_time(datetime.datetime.now())        
        values = {
          'shouts':shouts.fetch(size,offset),
          'url': url,
          'url_linktext': url_linktext,
          'pagestr': pagestr,
          'currpage':currpage,
          #'post_time': post_time       
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
        self.response.out.write(template.render(path, values))
        

    def post(self):
        
        shout = Shout(message=self.request.get('message'))
        avatar =  self.request.get("img")
        #avatar = images.resize(self.request.get("img"), 100, 100)
        

        shout.avatar = db.Blob(str(avatar))
        if users.get_current_user():
            shout.author = users.get_current_user()
        shout.put()
        mail.send_mail(sender="nnnnon@gmail.com",
                      to="马理军  <nnnnon+Appspot@gmail.com>",
                      subject="appspot 的信息",
                      body=self.request.get('message').encode('utf-8'))
                
        self.redirect('/')
class Image (webapp.RequestHandler):
    def get(self):
        shout = db.get(self.request.get("img_id"))
        if shout.avatar:
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.out.write(shout.avatar)
        else:
            self.response.out.write("No image")
#Anybody who had writed the blog has the right to edit it
class EditShout(webapp.RequestHandler):
  def get(self,sid):
    if users.get_current_user() == None :
      self.redirect(users.create_login_url(self.request.uri))
      
    shout = db.get(sid)
    if users.get_current_user() == shout.author \
                                or users.is_current_user_admin():
      template_values = {
        'shout': shout,
      }
      path = os.path.join(os.path.dirname(__file__), 
                              'template/edit_shout.html')
      self.response.out.write(template.render(path, template_values))
    else :
      self.redirect("/exception/hasnoright.html")

#Anybody who had writed the blog has the right to update it
class UpdateShout(webapp.RequestHandler):
  def post(self):
    if users.get_current_user() == None :
      self.redirect(users.create_login_url(self.request.uri))
      
    shout = db.get(self.request.get('key'))
    if users.get_current_user() == shout.author \
                    or users.is_current_user_admin():
      greeting.title = self.request.get('title')
      greeting.tags = self.request.get('tags').split(' ')
      greeting.content = self.request.get('content')
      
      greeting.put()
      self.redirect('/')
    else:
      self.redirect("/exception/hasnoright.html")
    
#Anybody who had writed the blog has the right to delete it
class DeleteShout(webapp.RequestHandler):
  def get(self,sid):
    shout = db.get(sid)
    page = self.request.get('p')
    if shout.author:
        if users.get_current_user():
            self.redirect("/exception/has_no_right.html")
        if users.get_current_user() == shout.author or users.is_current_user_admin():
            shout.delete()
            self.redirect('/?p='+page)
        else :
            self.redirect("/exception/has_no_right.html")
    else:
        if users.is_current_user_admin():
            shout.delete()
            self.redirect('/?p='+page)
        else:
            self.redirect("/exception/has_no_right.html")
        
        

def main():
    
    app = webapp.WSGIApplication([
    ('/',MyHandler),
    ('/img', Image),
    (r'/delete/(.*)', DeleteShout),
    ],debug=True)
    wsgiref.handlers.CGIHandler().run(app)

def modify_time(when):
    return when + datetime.timedelta(hours=8)
if __name__ == '__main__':
    #update('hello')
    main()
