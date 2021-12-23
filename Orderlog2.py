import requests
from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
import socket

# Link for CatalogServer since we need to communicate with it through REST
# This needs to be filled twice in terminal for some reason
BASE = input("Enter the Catalog IP Server only EX:192.168.1.123\n")
BASE2 = input("Enter the Orderlog IP Server only EX:192.168.1.123\n")
app = Flask(__name__)
api = Api(app)


# Purchase operation, it contains put method since we are updating
class purchase(Resource):

    # Put takes ID of item to buy as argument
    def put(self, idreq):
        # We ask the Catalog server to perform Query then Update.
        response = requests.put("http://" + BASE + ":8001/" + "update/" + idreq)
        # We add the order details that's returned to us to a TXT file that behaves as DB
        with open('orderlog2.txt', 'a') as f:
            f.write(response.text)
            f.write('\n')
            f.close()
        # We return the order ID after it's purchased successfully
        # InvokeConsistency for replica
        requests.put("http://" + BASE2 + ":5000/" + "purchase2/" + response.text)
        return "Item " + idreq + " purchased successfully"

# Consistency end point
class purchase2(Resource):

    # Put takes ID of item to buy as argument
    def put(self, idreq):
        with open('orderlog2.txt', 'a') as f:
            f.write(idreq)
            f.write('\n')
            f.close()



# Add resource end point link
api.add_resource(purchase, "/purchase/<string:idreq>")
api.add_resource(purchase2, "/purchase2/<string:idreq>")
# We run the Server on the PRIVATE SERVER IP which we can get through socket
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
