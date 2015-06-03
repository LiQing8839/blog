__author__ = 'Qing'
import MySQLdb
import json

from tornado.options import options
class DbModel(object):
    def __init__(self,timeout=60):
        self.host = options.dbhost
        self.port = options.dbport
        self.user = options.dbuser
        self.passwd = options.dbpasswd
        self.db = options.db
        self.charset = options.charset
        self.timeout = timeout

    def connect(self):
        try :
            self.conn = MySQLdb.connect(host = self.host,
                                        port = self.port,
                                        user = self.user,
                                        passwd = self.passwd,
                                        db =self.db,
                                        charset = self.charset,
                                        connect_timeout = self.timeout)
        except MySQLdb.OperationalError as e:
            raise e
        except MySQLdb.ProgrammingError as e:
            raise e

        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def commit(self,sql):
        try :
            num = self.cursor.execute(sql)
            self.conn.commit()
        except MySQLdb.OperationalError as e:
            self.conn.rollback()
            raise e
        except MySQLdb.ProgrammingError as e:
            self.conn.rollback()
            raise e
        return num

    def select(self,**kwargs):
        if not kwargs:
            #sql = "select * from t_blog where id=%s;"%kwargs["id"]
            sql = "select blog_name from t_blog order by create_time desc limit 10;"
        else :
            limit = (kwargs.has_key("limit") and kwargs["limit"]) and "limit %d" or ""

            sql = "select test from t_blog where %s;" %limit

            if limit == "limit 1":
                try :
                    self.cursor.execute(sql)
                except MySQLdb.OperationalError as e:
                    raise e
                except MySQLdb.ProgrammingError as e:
                    raise e
                data = self.cursor.fetchone()
                return json.dumps(data)


        try :
            self.cursor.execute(sql)
        except MySQLdb.OperationalError as e:
            raise e
        except MySQLdb.ProgrammingError as e:
            raise e
        data = []
        for i in self.cursor.fetchall():
            data.append(i)
        #return  json.dumps(data)
        return data

    def table(self,tablename):
        self.ping()
        try :
            self.cursor.execute("DESC %s;"%tablename)
        except MySQLdb.ProgrammingError as e:
            raise e

    def ping(self):
        try:
            self.conn.ping()
        except Exception:
            self.connect()
