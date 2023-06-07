from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

projects = [{
    'name': 'my first project',
    'tasks': [{
        'name': 'my first task',
        'completed': False
    }]
}, {
    'name': 'my second project',
    'tasks': [{
        'name': 'my second task',
        'completed': True
    }]
}]


@app.route("/")
def index_page():
  user_name = "George"
  return render_template('index.html.j2', name=user_name)


@app.route("/projects")
def project_list():
  return jsonify({"projects": projects})


# a route to create a project
@app.route("/project", methods=["POST"])
def create_project():
  request_data = request.get_json()
  if "name" not in request_data:
    return jsonify({"error": "no project name provided"}), 400
  if "tasks" not in request_data:
    return jsonify({"error": "no tasks provided"}), 400
  # we are creating a new project with the data we received from the request
  new_project = {"name": request_data["name"], "tasks": request_data["tasks"]}
  # we are adding the newly created project to the "database"
  projects.append(new_project)
  return jsonify(new_project)


# GET a project by name
@app.route("/project/<string:name>")
def get_project(name):
  # if the project name contains spaces, those will look like: %20
  # http://127.0.0.1:5000/project/my%20first%20project
  print(name)
  for project in projects:
    if project["name"] == name:
      return jsonify(project)
  return jsonify({"error": "project not found"}), 404


# add task to project endpoint:
@app.route("/project/<string:name>/task", methods=["POST"])
def add_task_to_project(name):
  request_data = request.get_json()
  for project in projects:
    if project["name"] == name:
      if "name" not in request_data:
        return jsonify({"error": "no task name provided"}), 400
      if "completed" not in request_data:
        return jsonify({"error": "no completed status provided"}), 400
      new_task = {
          # we are not checking the type of the data, we assume it is correct!
          # in production this is a bad idea, but for now we will assume that
          # the data is correct
          "name": request_data["name"],
          "completed": request_data["completed"]
      }
      project["tasks"].append(new_task)
      return jsonify(project)
  return jsonify({"error": "project not found"}), 404


# get all tasks in a project. The route defaults to GET Requests
# so we don't need to specify the method
@app.route("/project/<string:name>/tasks")
def get_all_tasks_in_project(name):
  for project in projects:
    if project["name"] == name:
      return jsonify({"tasks": project["tasks"]})
  return jsonify({"error": "project not found"}), 404
