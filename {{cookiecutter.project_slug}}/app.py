from flask import Flask, jsonify, request

app = Flask(__name__)

# this is for demo purposes. remove it when using for production use.
default_routes = [
    {
        'description': 'get all todos',
        'method': 'GET',
        'path': '/todos'
    },
    {
        'description': 'get details of a todo',
        'method': 'GET',
        'path': '/todos/<int:todo_id>'
    },
    {
        'description': 'create a new todo',
        'method': 'POST',
        'path': '/todos'
    }
    ,
    {
        'description': 'update a todo',
        'method': 'PUT',
        'path': '/todos/<int:todo_id>'
    }
    ,
    {
        'description': 'delete a todo',
        'method': 'DELETE',
        'path': '/todos/<int:todo_id>'
    }
]

# This is an in-memory store for the purposes of this example.
# You would typically use a database like MySQL or MongoDB in a real app.
todos = [
    {
        'id': 1,
        'todo': 'Try Planton Cloud',
        'completed': False
    },
    {
        'id': 2,
        'todo': 'Go To Market 5X Faster',
        'completed': False
    }
]

@app.route('/', methods=['GET'])
def get_default_routes():
    return jsonify(default_routes)

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next(filter(lambda t: t['id'] == todo_id, todos), None)
    if todo:
        return jsonify(todo)
    else:
        return 'Todo not found', 404

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = data['todo']
    if not todo or len(todo) < 3:
        return 'Todo must be at least 3 characters long', 400
    todo = {
        'id': todos[-1]['id'] + 1,
        'todo': todo,
        'completed': False
    }
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next(filter(lambda t: t['id'] == todo_id, todos), None)
    if not todo:
        return 'Todo not found', 404
    data = request.get_json()
    todo = data['todo']
    if not todo or len(todo) < 3:
        return 'Todo must be at least 3 characters long', 400
    todo['todo'] = todo
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = next(filter(lambda t: t['id'] == todo_id, todos), None)
    if not todo:
        return 'Todo not found', 404
    todos.remove(todo)
    return jsonify(todo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
