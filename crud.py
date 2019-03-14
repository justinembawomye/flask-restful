from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos ={}
class TodoSImple(Resource):
    def get(self, todo_id):
        return {todo_id:todos[todo_id]}
    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id:todos[todo_id]} 

class Todo2(Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201        

api.add_resource(Todo2, "/todo")
api.add_resource(TodoSImple, "/<string:todo_id>")
