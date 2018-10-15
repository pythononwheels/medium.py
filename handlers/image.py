#from medium.handlers.base import BaseHandler
from medium.handlers.powhandler import PowHandler
from medium.models.tinydb.image import Image as Model
from medium.config import myapp, database, server_settings
from medium.application import app
import simplejson as json
import tornado.web
import os
from werkzeug.utils import secure_filename

@app.add_route('/image/add/<uuid:article_id>', dispatch={"post" : "add_image"})
@app.add_rest_routes("image")
class Image(PowHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    # thru the @app.add_rest_routes() decorator.
    #
    # 1  GET    /image        #=> list
    # 2  GET    /image/1      #=> show
    # 3  GET    /image/new    #=> new
    # 4  GET    /image/1/edit #=> edit 
    # 5  GET    /image/page/1 #=> page
    # 6  GET    /image/search #=> search
    # 7  PUT    /image/1      #=> update
    # 8  PUT    /image        #=> update (You have to send the id as json payload)
    # 9  POST   /image        #=> create
    # 10 DELETE /image/1      #=> destroy
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
    hide_list=["id", "created_at", "last_updated"]
    
    @tornado.web.authenticated
    def add_image(self, article_id=None):
        print("add_image: :" + str(article_id))
        #print("request.files[file]: {}".format(str(self.request.files['file'])))
        print(str(self.request))
        image=Model()
        try:
            # {'files[]': [{'filename': 'bstrap_blog.PNG', 'body': b'\x89 ... '}]
            print("request.files[name]: {}".format(str(self.request.files["files[]"][0]["filename"])))
            file1 = self.request.files["files[]"][0]
        except Exception as e: 
            print(str(e))
        try:
            #file1_data = f["body"]
            #for key in file1.keys():
            #    print("key=>" + str(key))
            original_fname = file1['filename']
            fname, extension = os.path.splitext(original_fname)
            print("fname, extension :" + str(fname) + ", " + str(extension))
            image.articles.append(article_id)
            image.filename = fname
            image.extension = extension
            
            #fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
            sec_filename= secure_filename(original_fname)
            final_filename = os.path.join(myapp["upload_path"], sec_filename)
            output_file = open( final_filename, 'wb')
            output_file.write(file1['body'])
            try:
                image.upsert()
            except Exception as e: 
                print("error upserting image")
            #self.success(message="final_filename is uploaded", data=image, format="json")
            out_d = { "files" : [ { "url" : myapp["app_base_url"] + myapp["upload_url"] + "/" + sec_filename} ] }
            print(json.dumps(out_d))
            #self.write(json.dumps(out_d))
     
            self.success(pure=out_d, format="json")
            
        except Exception as e: 
            print("raw error: {}".format(str(e)) )
            self.error(message="Error uploading final_filename:" + str(e), format="json")

    def show(self, id=None):
        m=Model()
        res=m.find_by_id(id)
        self.success(message="image show", data=res)
    
    @tornado.web.authenticated
    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="image, index", data=res)         
    
    @tornado.web.authenticated
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="image page: #" +str(page), data=res )  
    
    @tornado.web.authenticated
    def search(self):
        m=Model()
        return self.error(message="image search: not implemented yet ")
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            self.success(message="image, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="image, edit id: " + str(id) + "msg: " + str(e) , data=None)
            
    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="image, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            m.upsert()
            self.success(message="image, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="image, error updating " + str(m.id) + "msg: " + str(e), 
                data=m, format="json")
    
    @tornado.web.authenticated
    def update(self, id=None):
        data_json = self.request.body
        m=Model()
        m.init_from_json(data_json)
        res = m.find_by_id(m.id)
        res.init_from_json(data_json)
        try:
            #res.tags= res.tags.split(",")
            res.upsert()
            self.success(message="image, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="image, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json")



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