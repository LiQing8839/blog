# -*- coding:utf8 -*-
import os.path
import MySQLdb
import logging

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
from tornado.options import define,options

from model.mysql_connect import DbModel

from views.index import IndexHandler ,HomeHandler,PageHandler,AboutHandler,QingHandler

define("port",default=8000,help="port of tornado web",type=int)
define("dbhost",default="114.215.176.153",help="mysql host",type=str)
define("dbport",default=3306,help="mysql port",type=int)
define("dbuser",default="root",help="mysql user",type=str)
define("dbpasswd",default="123456",help="mysql passwd",type=str)
define("db",default="test",help="mysql database",type=str)
define("charset",default="utf8",help="mysql charset",type=str)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",IndexHandler),
            (r"/home.html",HomeHandler),
            (r"/page.html",PageHandler),
            (r"/about.html",AboutHandler),
            (r"/Qing.html",QingHandler)

        ]

        settings = dict(
            template_path =  os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
        )

        tornado.web.Application.__init__(self,handlers,**settings)
        self.db = DbModel()
        self.db.connect()

if __name__=="__main__":
    logging.debug("debug...")
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
