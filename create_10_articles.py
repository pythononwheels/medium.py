#
# create 10 dummy articles
# 

from medium.models.tinydb.article import Article
from medium.models.tinydb.author import Author

def get_author(author_id):
        """
            returns a dict with the author information for the given author_id
        """
        a=Author()
        author = a.find_by_id(author_id)
        adict=author.to_dict()
        adict.pop("password")
        adict.pop("login")
        return adict


if __name__ == "__main__":
    a=Author()
    admin=get_author("f74c8108-55d1-4a61-8fa3-88b81e987e9d")

    for x in range(0,9):
        a = Article()
        a.title ="I am Article #" + str(x)
        a.author=admin
        a.author_id=admin["id"]
        a.teaser="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est"
        a.upsert()