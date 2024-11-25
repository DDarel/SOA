from flask import Flask # type: ignore
from flask_restful import Api, Resource # type: ignore
from formula import calculate_formula

app = Flask(__name__)
api = Api(app)

class Calculation(Resource):
    def get(self, user_id, weight):
        return {"user_id" : str(user_id), "water" : str(calculate_formula(weight))}

api.add_resource(Calculation, "/calculate/<int:user_id>/<float:weight>")

if __name__ == "__main__":
    app.run(host='172.31.38.25', port=5002, debug=True)