#coding:utf-8

from google.appengine.ext import db
import datetime
class Shout(db.Model):
    message = db.TextProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    #who = db.StringProperty()
    author = db.UserProperty() 
    avatar = db.BlobProperty()
    def modify_time(self):
        return (self.when + datetime.timedelta(hours=8))\
                    .strftime("%Y年%m月%d日 %H:%M:%S")
    def pic_key(self):
        return self.key()
