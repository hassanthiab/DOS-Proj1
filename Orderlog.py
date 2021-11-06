from datetime import timedelta
BASE = "http://127.0.0.1:8000/"
import requests
from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

class purchase(Resource):
    def put(self, idreq ):
        response = requests.put(BASE + "update/" + idreq)
        with open('orderlog.txt', 'a') as f:
            f.write(response.text)
            f.write('\n')
            f.close()
        return "Item "+idreq+" purchased successfully"





api.add_resource(purchase, "/purchase/<string:idreq>")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)