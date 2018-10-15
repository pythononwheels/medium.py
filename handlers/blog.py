#from medium.handlers.base import BaseHandler
from medium.handlers.powhandler import PowHandler
from medium.config import myapp
from medium.application import app
import simplejson as json
import tornado.web
from tornado import gen
# Please import your model here. (from yourapp.models.dbtype)
from medium.models.tinydb.article import Article


#@app.add_route('/blog/<int:page>', dispatch={"get" : "blog_page"})
#@app.add_route('/blog', dispatch={"get" : "blog_main"})
class Blog(PowHandler):
    #
    # on HTTP GET this method will be called. See dispatch parameter.
    #
    def blog_main(self):
        """
            Blog main => show the blog, iterate over all articles
            for now without a paging limit
        """ 
        a = Article()
        res = a.find_all()
        curr_user=self.current_user
        #if user:
        #    curr_user=user.login
        #else:
        #    curr_user=None
        self.success(message="blog_main()", data=list(res), model=a, template="index_medium.bs4", curr_user=curr_user)
        #self.write("I got testval:" + str(testval))
    
    def blog_page(self, page=0):
        """
            show blog main->page x
        """
        self.write("shop page: " + str(page))
    
