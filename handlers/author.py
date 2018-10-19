#from medium.handlers.base import BaseHandler
from medium.handlers.powhandler import PowHandler
from medium.models.tinydb.author import Author as Model
from medium.models.tinydb.article import Article
from medium.config import myapp, database
from medium.application import app
import simplejson as json
import tornado.web

@app.add_rest_routes("author")
class Author(PowHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    # thru the @app.add_rest_routes() decorator.
    #
    # 1  GET    /author        #=> list
    # 2  GET    /author/1      #=> show
    # 3  GET    /author/new    #=> new
    # 4  GET    /author/1/edit #=> edit 
    # 5  GET    /author/page/1 #=> page
    # 6  GET    /author/search #=> search
    # 7  PUT    /author/1      #=> update
    # 8  PUT    /author        #=> update (You have to send the id as json payload)
    # 9  POST   /author        #=> create
    # 10 DELETE /author/1      #=> destroy
    #

    # standard supported http methods are:
    # SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    # you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    # handler.

    # curl test:
    # windows: (the quotes need to be escape in cmd.exe)
    #   (You must generate a post model andf handler first... update the db...)
    #   POST:   curl -H "Content-Type: application/json" -X POST -d "{ \"title\" : \"first post\" }" http://localhost:8080/post
    #   GET:    curl -H "Content-Type: application/json" -X GET http://localhost:8080/post
    #   PUT:    curl -H "Content-Type: application/json" -X PUT -d "{ \"id\" : \"1\", \"text\": \"lalala\" }" http://localhost:8080/post
    #   DELETE: curl -H "Content-Type: application/json" -X DELETE -d "{ \"id\" : \"1\" }" http://localhost:8080/post
    
    model=Model()
    
    # these fields will be hidden by scaffolded views:
    hide_list=[ "created_at", "last_updated","password"]

    @tornado.web.authenticated
    def show(self, id=None):
        m=Model()
        res=m.find_by_id(id)
        self.success(message="author show", data=res)
    
    @tornado.web.authenticated
    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="author, index", data=res)         
    
    @tornado.web.authenticated
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="author page: #" +str(page), data=res )  
    
    @tornado.web.authenticated
    def search(self):
        m=Model()
        return self.error(message="author search: not implemented yet ")
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            print("edit: calling success!! . res=" + str(res))
            self.success(message="author, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="author, edit id: " + str(id) + "msg: " + str(e) , data=None)

    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="author, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            m.password=self.generate_password_hash(m.password)
            m.upsert()
            self.success(message="author, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="author, error updating " + str(m.id) + "msg: " + str(e), 
                data=m, format="json")
    
    @tornado.web.authenticated
    def update(self, id=None):
        data_json = self.request.body
        m=Model()
        m.init_from_json(data_json)
        res = m.find_by_id(m.id)
        res.init_from_json(data_json)
        #
        # update all author dicts in articles of this author
        #
        art=Article()
        author_articles=art.find(art.where("author_id") == res.id, as_generator=True)
        for elem in author_articles:
            elem.author=res.to_dict()
            elem.upsert()
            print("updated author information for article: {}".format(str(elem.id)) )

        try:
            #res.tags= res.tags.split(",")
            res.upsert()
            self.success(message="author, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="author, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json")



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