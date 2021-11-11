from datetime import timedelta

from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import socket
# We connect the SQLAlchemy to DB created by SQLITE3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)
api = Api(app)
db = SQLAlchemy(app)


# Storage Model for the DB we created. We have ID be unique
class Storage(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Book(topic={self.topic},name={self.name},  cost={self.cost}, stock={self.stock})"


# Create DB
db.create_all()

# Resource fields makes the output we get seralizable into JSON. Without we can't turn the file into a JSON format
resource_fields = {
    'ID': fields.Integer,
    'name': fields.String,
    'topic': fields.String,
    'stock': fields.Integer,
    'cost': fields.Integer,

}


# Search operation that returns all the items that match a specific topic
class Search(Resource):
    @marshal_with(resource_fields)
    def get(self, topicreq):
        # We use SQLAlchemy functions and query then filter by TOPIC, then ALL to return all items matching it
        result = Storage.query.filter_by(topic=topicreq).all()
        return result


# Info operation that gives all information related to a specific ID
class Info(Resource):
    @marshal_with(resource_fields)
    def get(self, idreq):
        # We filter again but this time by ID then return the first matching ID
        result = Storage.query.filter_by(ID=idreq).first()
        return result


# Update Operation that first Queries the DB for a specific ID then updates it by deducting 1. If it reaches 0 we add 5
class Update(Resource):
    @marshal_with(resource_fields)
    def put(self, idreq):
        # Filter by ID and get first item. -1 the stock attribute. If it's 0 update stock by 5 then commit.
        result = Storage.query.filter_by(ID=idreq).first()
        result.stock = result.stock - 1
        if result.stock == 0:
            result.stock = 5
        db.session.commit()
        return result


# Three end points for the operations the server is meant to execute.

api.add_resource(Search, "/search/<string:topicreq>")
api.add_resource(Info, "/info/<int:idreq>")
api.add_resource(Update, "/update/<int:idreq>")
# We run the Server on the PRIVATE SERVER IP which we can get through socket
if __name__ == "__main__":
    app.run(host=socket.gethostbyname(socket.gethostname()+".local"), port=8000, debug=True)
