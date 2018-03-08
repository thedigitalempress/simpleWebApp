import tornado.ioloop
import tornado.web

users = {"Empress": "digital"}

class SysStatusHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("user"):
            self.redirect("/login")
            return
        if self.get_argument("type") == "processes":
            com = [["pstree"], ["top", "-bn1"]]
        elif self.get_argument("type") == "system":
            com = [["uname", "-a"], ["uptime"]]
        elif self.get_argument("type") == "syslog":
            com = [["tail", "-n100", "/var/log/syslog"]]
        elif self.get_argument("type") == "storage":
            com = [["df", "-h"], ["free"]]
        elif self.get_argument("type") == "network":
            com = [["ifconfig"]]
        else:
            com = [["df", "-h"], ["free"], ["uname", "-a"], ["who"], ["uptime"], ["tail", "/var/log/syslog"], ["pstree"], ["top", "-bn1"]]
        self.render("sysstatus-template.html", commands = com)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login-template.html")

        def post(self):
            print(self.get_argument("name"))
            print(self.get_argument("password"))
            if self.get_argument("name") in users.keys() and users[self.get_argument("name")] == self.get_argument("password"):
                self.set_secure_cookie("user", self.get_argument("name"))
                self.redirect("/sysstatus?type=system")
            else:
                self.render("login-fail.html")

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.render("logout-template.html")

if __name__ == "__main__":
    application = tornado.web.Application([
    (r"/login", LoginHandler),
    (r"/sysstatus", SysStatusHandler),
    (r"/logout", LogoutHandler),
    ], cookie_secret="put your own random text here")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
