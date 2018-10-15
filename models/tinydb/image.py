#
# TinyDB Model:  Image
#
from medium.models.tinydb.tinymodel import TinyModel

class Image(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'filename'  :    { 'type': 'string', 'maxlength' : 255},
        'extension' :    { 'type': 'string'},
        'mime_type' :    { 'type': 'string'},
        'articles'  :    { 'type': 'list', "default" : [] },
        "tags"      :    { 'type': 'list', "default" : [] }
        }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
