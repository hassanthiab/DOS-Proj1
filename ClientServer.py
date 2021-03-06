from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
import socket
import requests
import redis
import json

# Link for CatalogServer & Orderlogsince we need to communicate with it through REST.
# This needs to be filled twice in terminal for some reason

app = Flask(__name__)
api = Api(app)
BASE = input("Enter the Catalog IP Server only EX:192.168.1.123\n")
BASE2 = input("Enter the Orderlog IP Server only EX:192.168.1.123\n")
BASE3 = input("Enter the Catalog IP2 Server only EX:192.168.1.123\n")
BASE4 = input("Enter the Orderlog IP2 Server only EX:192.168.1.123\n")
y = 1
x = 0
cache_data = {}


# Redirects the purchase Operation once triggered towards Orderlog with the ID requested and returns the response as TXT
class purchase(Resource):

    def put(self, idreq):
        global x
        # Load balancing, first request goes to one then second to two and loop back
        if x == 0:
            response = requests.put("http://" + BASE2 + ":5000/" + "purchase/" + idreq)
            x = 1
        else:
            response = requests.put("http://" + BASE4 + ":5001/" + "purchase/" + idreq)
            x = 0
        return response.text


# Redirects the Search operation once triggered towards Catalog with the TOPIC requested, returns response JSON
class Search(Resource):
    def get(self, topicreq):
        global y
        global cache_data

        # Check if it's in cache
        if topicreq in cache_data:
            return cache_data[topicreq]
        else:
            # Load balancing for replicas requests as before
            if y == 0:
                response = requests.get("http://" + BASE + ":8000/" + "search/" + topicreq)
                # Write data onto cache with TOPIC as key
                cache_data[topicreq] = response.text
                y = 1
            else:
                response = requests.get("http://" + BASE3 + ":8001/" + "search/" + topicreq)
                # Write data onto cache with TOPIC as key
                cache_data[topicreq] = response.text
                y = 0

            return response.json()


# Redirects the Info operation once triggered towards Catalog with the ID requested, returns response JSON
class Info(Resource):
    def get(self, idreq):
        global cache_data
        # check if in cache
        if idreq in cache_data:
            return cache_data[idreq]
        else:
            #LOAD BALANCE AS BEFORE
            global y
            if y == 0:
                response = requests.get("http://" + BASE + ":8000/" + "info/" + idreq)
                # Write data onto cache with ID as key
                cache_data[idreq] = response.text

                y = 1
            else:
                response = requests.get("http://" + BASE3 + ":8001/" + "info/" + idreq)
                # Write data onto cache with ID as key
                cache_data[idreq] = response.text
                y = 0

            return response.json()

# Remove all keys that match ID from cache
class cache(Resource):

    def put(self, idreq):
        del cache_data[idreq]

# Remove all Keys that match the TOPICREQ from cache dictionary
class cache2(Resource):

    def put(self, topicreq):
        del cache_data[topicreq]


# Add resource end point link

api.add_resource(Search, "/search/<string:topicreq>")
api.add_resource(Info, "/info/<string:idreq>")
api.add_resource(purchase, "/purchase/<string:idreq>")
api.add_resource(cache, "/cache/<string:idreq>")
api.add_resource(cache2, "/cache2/<string:topicreq>")
# We run the Server on the PRIVATE SERVER IP which we can get through socket
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000, debug=True)
