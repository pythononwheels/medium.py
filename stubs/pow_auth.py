#
# Basic PoW Auth class 
#
import werkzeug.security 
from {{appname}}.models.tinydb import pow_user as Model
class PowAuth(object):
    
    def check_auth( login, pwd ):
        """
            checks the login, password hash combination
            against the pow_user model
        """
        m = Model()
        try:
            m = m.find(m.Query.login == login )
        except:
            return (False, "Cant find user: " + login) 
        try:
            return werkzeug.security.check_password_hash(m.pwd_hash, pwd )
        except:
            return (False, "Wrong password for user: " + login) 
