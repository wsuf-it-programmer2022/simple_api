from flask import Flask, render_template, jsonify

app = Flask(__name__)

projects = [{
    'name': 'my first project',
    'tasks': [{
        'name': 'my first task',
        'completed': False
    }]
}]


@app.route("/")
def index_page():
  user_name = "George"
  return render_template('index.html.j2', name=user_name)


@app.route("/projects")
def project_list():
  return jsonify({"projects": projects})
