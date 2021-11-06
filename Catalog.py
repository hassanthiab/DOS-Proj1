from datetime import timedelta

from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)
api = Api(app)

db = SQLAlchemy(app)


class Storage(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=True)

    def __repr__(self):

        return f"Book(topic={self.topic},name={self.name},  cost={self.cost}, stock={self.stock})"


db.create_all()
resource_fields = {
    'ID': fields.Integer,
    'name': fields.String,
    'topic': fields.String,
    'stock': fields.Integer,
    'cost': fields.Integer,

}


class Search(Resource):
    @marshal_with(resource_fields)
    def get(self, topicreq):
        result = Storage.query.filter_by(topic=topicreq).all()
        return result
class Info(Resource):
    @marshal_with(resource_fields)
    def get(self, idreq):
        result = Storage.query.filter_by(ID=idreq).first()
        return result
class Update(Resource):
    @marshal_with(resource_fields)
    def put(self, idreq):
        result = Storage.query.filter_by(ID=idreq).first()
        result.stock = result.stock-1
        if result.stock==0:
            result.stock=5
        db.session.commit()
        return result


api.add_resource(Search, "/search/<string:topicreq>")
api.add_resource(Info, "/info/<int:idreq>")
api.add_resource(Update, "/update/<int:idreq>")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
