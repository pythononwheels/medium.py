#
# TinyDB Model:  Stundenplan
#
from medium.models.tinydb.tinymodel import TinyModel

class Stundenplan(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'Stunde':    { 'type': 'string', 'maxlength' : 35},
        'Montag' :    { 'type': 'string'},
        'Dienstag' :    { 'type': 'string'},
        'Mittwoch' :    { 'type': 'string'},
        'Donnerstag' :    { 'type': 'string'},
        'Freitag' :    { 'type': 'string'},   
        }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
