# -*- coding:utf8 -*-
__author__ = 'Qing'
import tornado.web
from model.mysql_connect import DbModel
import json



class BaseHandler(tornado.web.RequestHandler):
    def __init__(self,*args,**kwargs):
        super(BaseHandler,self).__init__(*args,**kwargs)

    @property
    def db(self):
        return self.application.db

    def initialize(self):
        self.title = "Qing的博客"


class IndexHandler(BaseHandler):

    def get(self):
        self.render("index.html",web_title = self.title,error = "")


class HomeHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        title_name=[]
        self.db.table("t_blog")
        #sql = "select blog_name from t_blog;"
        data = self.db.select()
        #print data
        #title_name = data[0]["blog_name"]
        for l in range(len(data)):
            title_name.append(data[l]["blog_name"])

        self.render("home.html",web_title = self.title,error = "",title_name=title_name)

class PageHandler(BaseHandler):
    def get(self):
        value = self.get_argument('id',None)
        data = self.db.select(value)
        self.render("page.html",data=data)


class AboutHandler(BaseHandler):
    def get(self):
        self.render('about.html')

class QingHandler(BaseHandler):
    def get(self):
        self.render("Qing.html")