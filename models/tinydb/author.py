#
# TinyDB Model:  Author
#
from medium.models.tinydb.tinymodel import TinyModel
import werkzeug.security 
from medium.config import myapp 

class Author(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'firstname' :    { 'type': 'string', 'maxlength' : 30},
        'lastname'  :    { 'type': 'string', 'maxlength' : 30},
        'login'     :    { 'type': 'string', 'maxlength' : 15},
        'password'  :    { 'type': 'string'},
        'email'     :    { 'type': 'string', 'maxlength' : 40},
        'description' :  { 'type': 'string', 'maxlength' : 60},
        'screenname':    { 'type': 'string', 'maxlength' : 15},
        'homepage'  :    { 'type': 'string'},
        'twitter'   :    { 'type': 'string'},
        'github'    :    { 'type': 'string'},
        "gravatar"  :    { "type": "string"},
        'articles'  :    { 'type': 'list', "default" : [] }
        }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
    def check_password_hash(self, pwhash, password ):
        """
            uses werkzeug.security.check_password_hash
            see: http://werkzeug.pocoo.org/docs/0.14/utils/#module-werkzeug.security
            get the password from for example a login form (make sure you use https)
            get the hash from the user model table (see generate_password_hash below)
        """
        return werkzeug.security.check_password_hash(pwhash, password)

    def generate_password_hash(self,  password ):
        """
            uses werkzeug.security.generate_password_hash 
            see: http://werkzeug.pocoo.org/docs/0.14/utils/#module-werkzeug.security
            store this returned hash in the user models table as password
            when the user is first registered or changed his password.
            Use https to secure the plaintext POSTed pwd.
        """
        method = myapp["pwhash_method"]
        return werkzeug.security.generate_password_hash(password, method=method, salt_length=8)