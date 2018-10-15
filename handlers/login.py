#from medium.handlers.base import BaseHandler
from medium.handlers.powhandler import PowHandler
from medium.config import myapp
from medium.application import app
import simplejson as json
import tornado.web
from tornado import gen
# Please import your model here. (from yourapp.models.dbtype)
from medium.models.tinydb.author import Author

@app.add_route('/login/check', dispatch={"post" : "check"})
@app.add_route('/login', dispatch={"get" : "_get_method"})
@app.add_route('/logout', dispatch={"get" : "logout"})
class Login(PowHandler):
    #
    # on HTTP GET this method will be called. See dispatch parameter.
    #
    def _get_method(self):
        """
            just a simple hanlder sceleton. Adapt to your needs
        """ 
        #out_dict = {"testval" : str(testval)}
        #self.success(message="I got testval:", data=out_dict, format="json", raw_data=True)
        #self.write("I got testval:" + str(testval))
        if not self.get_secure_cookie("pow_blog_login"):  
            print("cookie not found")      
            self.render("login.bs4")
        else:
            print("already logged in")
            self.redirect("/blog")
    
    def logout(self):
        """
            logging out by simply deleting the cookie
        """
        try:
            self.clear_cookie("pow_blog_login")            
        except:
            pass # should not happen since logout link only shows when logged in
        self.redirect("/")

    def check(self):
        #print(str(self.request))
        if not self.get_secure_cookie("pow_blog_login"):
            # not already logged in
            login = self.get_body_argument("inputLogin", default=None, strip=False)
            password=self.get_body_argument("inputPassword", default=None, strip=False)
            a = Author()
            res = a.find(a.Query.login == login)
            check = self.check_password_hash(res.password, password)
            if check:
                print("seeting the login cookie now")
                self.set_secure_cookie("pow_blog_login", str(res.id))
                #self.render("index.tmpl", message="You successfully logged in")
                self.redirect("/")
            else:
                self.error(message="Sorry, could not log you in! Wrong user or password")
                #self.write("login:" + str(login) + "<br> password: " + str(password ))
        else:
            print("cookie already set! skipping.")
