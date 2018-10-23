#from medium.handlers.base import BaseHandler
from medium.handlers.powhandler import PowHandler
from medium.models.tinydb.article import Article as Model
from medium.models.tinydb.author import Author
from medium.config import myapp, database
from medium.application import app
import simplejson as json
import tornado.web

from medium.models.tinydb.author import Author
import datetime
@app.add_rest_routes("article")
@app.add_route("/article/<uuid:id>/upvote", dispatch={"put": "upvote"})
@app.add_route("/article/list/author/<uuid:id>", dispatch={"get": "list_author_articles"})
@app.add_route("/article/<uuid:id>/comment", dispatch={"post": "add_side_comment"})
@app.add_route("/blog_medium", dispatch={"get" : "blog_medium"})
@app.add_route("/blog_simple", dispatch={"get" : "blog_simple"})
class Article(PowHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    # thru the @app.add_rest_routes() decorator.
    #
    # 1  GET    /article        #=> list
    # 2  GET    /article/1      #=> show
    # 3  GET    /article/new    #=> new
    # 4  GET    /article/1/edit #=> edit 
    # 5  GET    /article/page/1 #=> page
    # 6  GET    /article/search #=> search
    # 7  PUT    /article/1      #=> update
    # 8  PUT    /article        #=> update (You have to send the id as json payload)
    # 9  POST   /article        #=> create
    # 10 DELETE /article/1      #=> destroy
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
    hide_list=["created_at", "last_updated", "text", "lead_image", "images", "published_date",
        "author_avatar", "author_twitter", "author_screenname", "comments", "featured_image", "voter_ips"]

    def add_side_comment(self, id):
        """
            adding a side comment for this article / paragraph
        """
        try:
            m=Model()
            current_article=m.find_by_id(id)
            data = self.request.body
            print(data)
            data=json.loads(data)
            print()
            section_id=data["sectionId"]
            data.pop("sectionId")
            
            if str(section_id) in current_article.side_comments:
                #there are already comments for this section
                 current_article.side_comments[str(section_id)].append(data)
            else:
                # first section comment
                current_article.side_comments[str(section_id)] = [data]
            current_article.upsert()
            print(current_article.side_comments)
        except Exception as e:
            self.error(message="Error adding comment. No such aricle id ??: " + str(id) + "msg: " + str(e) , data=None, status="500")

    def list_author_articles(self, id = None):
        """
            list all articles of author with given id
        """
        if id:
            a=Author()
            m=Model()
            author = a.find_by_id(id)
            author_articles=m.find(m.where("author_id") == author.id, as_generator=True)
            self.success( data=author_articles, curr_user=self.current_user, author=author )
        else:
            self.error(message="article, edit id: " + str(id) + "msg: " + str(e) , data=None, status="500")

    def get_sec_author_dict(self, author_id):
        """
            returns a dict with the author information for the given author_id
        """
        a=Author()
        author = a.find_by_id(author_id)
        adict=author.to_dict()
        adict.pop("password")
        adict.pop("login")
        return adict

    def blog_medium(self):
        """
            show the featured blog view
        """
        m=Model()
        res=m.find_all()
        self.success(message="blog medium", data=res, curr_user=self.current_user, template="index_medium.bs4")
    
    def blog_simple(self):
        """
            shows a simple blog styled article list
        """
        m=Model()
        res=m.find_all()
        self.success(message="blog simple", data=res, curr_user=self.current_user)

    def upvote(self, id=None):
        """
            vote the article one up
        """
        m=Model()
        current_article=m.find_by_id(id)
        current_article.votes+=1
        
        try:
            ip = self.request.remote_ip
            if ip not in current_article.voter_ips:
                current_article.voter_ips.append(ip)
        except:
            self.application.log_request(message="Error: Article.upvote: Could not get remote_ip: " + self.request.remote_ip)
        
        if current_article.votes > 10000:
            self.success(pure=True,format="json", data={"votes" : ">10k"}, message="successfully upvoted")
        else:
            current_article.upsert()
            self.application.log_request(self, message="Article.upvote: remote_ip: " + self.request.remote_ip)
            self.success(pure=True, format="json", data={"votes" : current_article.votes}, message="successfully upvoted")
            
        #else:
        #    print("ERROR: you can only vote once")
        #    self.error(pure=True, format="json", data={"message" : "you can only vote once"} )

    def show(self, id=None):
        m=Model()
        article=m.find_by_id(id)
        #adict = self.get_author(article.author_id)
        self.success(message="article show", data=article, curr_user=self.current_user)
    
    @tornado.web.authenticated
    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="article, index", data=res, curr_user=self.current_user)         
    
    @tornado.web.authenticated
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="article page: #" +str(page), data=res )  
    
    def search(self):
        m=Model()
        return self.error(message="article search: not implemented yet ")
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            self.success(message="article, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="article, edit id: " + str(id) + "msg: " + str(e) , data=None)

    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="article, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            auth_dict = self.current_user.to_dict()
            auth_dict.pop("login")
            auth_dict.pop("password")
            m.author=auth_dict
            m.author_id=auth_dict["id"]
            m.published_date=datetime.datetime.utcnow()
            m.upsert()
            self.success(message="article, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="article, error creating " + str(m.id) + "msg: " + str(e), 
                data=m, format="json")
    
    @tornado.web.authenticated
    def update(self, id=None):
        data_json = self.request.body
        m=Model()
        res = m.find_by_id(id)
        res.init_from_json(data_json,  simple_conversion=True)
        print(res.side_comments)
        print(type(res.side_comments))
        try:
            #res.tags= res.tags.split(",")
            res.upsert()
            self.success(message="article, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="article, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json", raw_data=True)



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