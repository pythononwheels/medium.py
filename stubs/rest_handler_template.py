#from {{appname}}.handlers.base import BaseHandler
from {{appname}}.handlers.powhandler import PowHandler
from {{appname}}.models.{{model_type}}.{{handler_name}} import {{handler_model_class_name}} as Model
from {{appname}}.config import myapp, database
from {{appname}}.application import app
import simplejson as json
import tornado.web

@app.add_rest_routes("{{handler_name}}")
class {{handler_class_name}}(PowHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    # when you add the : app.add_rest_routes() decorator.
    #
    # 1  GET    /todo                           #=> list
    # 2  GET    /todo/<uuid:identifier>         #=> show
    # 3  GET    /todo/new                       #=> new
    # 4  GET    /todo/<uuid:identifier>/edit    #=> edit 
    # 5  GET    /todo/page/<uuid:identifier>    #=> page
    # 6  GET    /todo/search                    #=> search
    # 7  PUT    /todo/<uuid:identifier>         #=> update
    # 8  PUT    /todo                           #=> update (You have to send the id as json payload)
    # 9  POST   /todo                           #=> create
    # 10 DELETE /todo/<uuid:identifier>         #=> destroy
    #
    
    # standard supported http methods are:
    # SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    # you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    # handler.

    # curl test:
    # windows: (the quotes need to be escape in cmd.exe)
    #   (You must generate a post model andf handler first... update the db...)
    #   POST:   curl -H "Content-Type: application/json" -X POST -d "{ \"title\" : \"first {{handler_name}}\" }" http://localhost:8080/{{handler_name}}
    #   GET:    curl -H "Content-Type: application/json" -X GET http://localhost:8080/{{handler_name}}
    #   PUT:    curl -H "Content-Type: application/json" -X PUT -d "{ \"id\" : \"1\", \"text\": \"lalala\" }" http://localhost:8080/{{handler_name}}
    #   DELETE: curl -H "Content-Type: application/json" -X DELETE -d "{ \"id\" : \"1\" }" http://localhost:8080/{{handler_name}}
    
    model=Model()
    
    # these fields will be hidden by scaffolded views:
    hide_list=["id", "created_at", "last_updated"]

    def show(self, id=None):
        m=Model()
        res=m.find_by_id(id)
        self.success(message="{{handler_name}} show", data=res)
        
    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="{{handler_name}}, index", data=res)         
    
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="{{handler_name}} page: #" +str(page), data=res )  
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            self.success(message="{{handler_name}}, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="{{handler_name}}, edit id: " + str(id) + "msg: " + str(e) , data=None)

    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="{{handler_name}}, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            m.upsert()
            self.success(message="{{handler_name}}, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="{{handler_name}}, error updating " + str(m.id) + "msg: " + str(e), 
                data=m, format="json")
    
    @tornado.web.authenticated
    def update(self, id=None):
        data_json = self.request.body
        m=Model()
        res = m.find_by_id(id)
        res.init_from_json(data_json, simple_conversion=True)
        try:
            #res.tags= res.tags.split(",")
            res.upsert()
            self.success(message="{{handler_name}}, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="{{handler_name}}, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json")



    @tornado.web.authenticated
    def destroy(self, id=None):
        try:
            data_json = self.request.body
            print("  .. DELETE Data: ID:" + str(data_json))
            m=Model()
            m.init_from_json(data_json)
            res = m.find_by_id(m.id)
            res.delete()
            self.success(message="todo, destroy id: " + str(m.id))
        except Exception as e:
            self.error(message="todo, destroy id: " + str(e))
    
    def search(self):
        m=Model()
        return self.error(message="{{handler_name}} search: not implemented yet ")