#
# TinyDB Model:  Article
#
from medium.models.tinydb.tinymodel import TinyModel
import datetime

class Article(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'title'          :   { 'type' : 'string', 'maxlength' : 255},
        'teaser'         :   { 'type' : 'string' },
        'text'           :   { 'type' : 'string'},
        'tags'           :   { 'type' : 'list', "default" : [] },
        'comments'       :   { 'type' : 'list', "default" : [] },
        'featured'       :   { 'type' : 'boolean', "default" : False },
        'blog'           :   { 'type' : 'boolean', "default" : False },   # True => article will show uip in blog view
        "votes"          :   { "type" : "integer", "default" : 0 },
        "author"         :   { "type" : "dict" }, #author 
        "author_id"      :   { "type" : "string" }, #author 
        "images"         :   { "type" : "list"  }, #list of images uploaded for this article   
        "featured_image" :   { "type" : "string", "default" : "" },
        "read_time"      :   { "type" : "string"},
        "published"      :   { "type" : "boolean"},
        "published_date" :   { "type" : "datetime", "default" : datetime.datetime(1999,1,1,23,59)},
        "voter_ips"      :   { "type" : "list", "default" : [] }
    }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
