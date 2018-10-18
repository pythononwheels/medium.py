import tornado.ioloop
import tornado.web
from medium.handlers.base import BaseHandler
from medium.application import app

# you can use regex in the routes as well:
# (r"/([^/]+)/(.+)", ObjectHandler),
# any regex goes. any group () will be handed to the handler 
# 

# if you specify a method, this method will be called for this route
# if you DON't specify a method, the standard HTTP verb method (e.g. get(), put() will be called)
@app.add_route("/", pos=1, dispatch={"get" : "index"})
@app.add_route("/getting_started", pos=1, dispatch={"get" : "getting_started"})
class IndexdHandler(BaseHandler):
    def index(self):
        #self.render("index.tmpl")
        #self.redirect("/article/list")
        self.redirect("/article/4491e852-b4bd-444f-a812-5c48a7b7af53")

    
# this will be the last route since it has the lowest pos.
@app.add_route(".*", pos=0)
class ErrorHandler(BaseHandler):
    def get(self):
        return self.error( template="404.tmpl", http_code=404  )

