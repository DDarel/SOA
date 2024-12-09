from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:004039Vlad@user-database.cn8m0yeugq4j.eu-central-1.rds.amazonaws.com:5432/user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
		return f"User(name = {name}, email = {email}, weight = {weight})" # type: ignore


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("email", type=str, help="User email", required=True)
user_put_args.add_argument("password", type=str, help="User password", required=True)
user_put_args.add_argument("name", type=str, help="User name", required=True)
user_put_args.add_argument("age", type=int, help="User age", required=True)
user_put_args.add_argument("weight", type=float, help="User weight", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("email", type=str, help="User email")
user_update_args.add_argument("password", type=str, help="User password")
user_update_args.add_argument("name", type=str, help="User name")
user_update_args.add_argument("age", type=int, help="User age")
user_update_args.add_argument("weight", type=float, help="User weight")


resource_fields = {
	'id': fields.Integer,
	'email': fields.String,
	'password': fields.String,
	'name': fields.String,
    'age': fields.Integer,
    'weight': fields.Float
}

class UserDB(Resource):
    
    @marshal_with(resource_fields)
    def get(self, user_id=None):
        email = request.args.get("email")

        if email:
            result = UserModel.query.filter_by(email=email).first()
            if not result:
                abort(404, message="Could not find user with that email")
        elif user_id is not None:
            result = UserModel.query.filter_by(id=user_id).first()
            if not result:
                abort(404, message="Could not find user with that id")
        else:
            abort(400, message="Either user_id or email must be provided")

        return result
    
    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        # result = UserModel.query.filter_by(id=user_id).first()
        # if result:
        #     abort(409, message="User id taken...")

        user = UserModel(email=args['email'], password=args['password'], name=args['name'], age=args['age'], weight=args['weight'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    
    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update")
        if args['email']:
            result.email = args['email']
        if args['password']:
            result.password = args['password']
        if args['name']:
            result.name = args['name']
        if args['age']:
            result.age = args['age']
        if args['weight']:
            result.weight = args['weight']

        db.session.commit()
        return result

    def delete(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User doesn't exist, cannot delete")
        db.session.delete(result)
        db.session.commit()
        return "Success deleted user with id : " + str(user_id) , 201

api.add_resource(UserDB, "/userDB/<int:user_id>")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001, debug=True)
