from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
import socket
import requests

# Link for CatalogServer & Orderlogsince we need to communicate with it through REST.
# This needs to be filled twice in terminal for some reason
BASE = input("Enter the Catalog IP Server only EX:192.168.1.123\n")
BASE2 = input("Enter the Orderlog IP Server only EX:192.168.1.123\n")
app = Flask(__name__)
api = Api(app)


# Redirects the purchase Operation once triggered towards Orderlog with the ID requested and returns the response as TXT
class purchase(Resource):
    def put(self, idreq):
        response = requests.put("http://" + BASE2 + ":5000/" + "purchase/" + idreq)
        return response.text


# Redirects the Search operation once triggered towards Catalog with the TOPIC requested, returns response JSON
class Search(Resource):
    def get(self, topicreq):
        response = requests.get("http://" + BASE + ":8000/" + "search/" + topicreq)
        return response.json()


# Redirects the Info operation once triggered towards Catalog with the ID requested, returns response JSON
class Info(Resource):
    def get(self, idreq):
        response = requests.get("http://" + BASE + ":8000/" + "info/" + idreq)
        return response.json()


# Add resource end point link

api.add_resource(Search, "/search/<string:topicreq>")
api.add_resource(Info, "/info/<string:idreq>")
api.add_resource(purchase, "/purchase/<string:idreq>")
# We run the Server on the PRIVATE SERVER IP which we can get through socket
if __name__ == "__main__":
    app.run(host=socket.gethostbyname(socket.gethostname() + ".local"), port=6000, debug=True)
