from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Instanciar la clase
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@localhost/flaskmysql"
# No tira warning cuando ejecutamos el programa
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Le paso la config al ORM
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Heredo propiedades de la instancia de db
class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self,title,description):
        self.title = title
        self.description = description

# Lee todas las cosas y crea tablas a partir de esas
# Crear todas las tablas dentro del contexto de la aplicación
with app.app_context():
    db.create_all()


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id","title","description")

# Interactúa con una sola tarea
task_schema = TaskSchema()
# Interactúa con muchas tareas
tasks_schema = TaskSchema(many=True)

@app.route("/tasks", methods=["POST"])
def create_task():
    # Recibo los datos del cliente
    title = request.json["title"]
    description = request.json["description"]

    # Creo una tarea y la guardo en base de datos
    new_task = Task(title,description)
    db.session.add(new_task)
    db.session.commit()

    # Respondemos tarea del cliente
    return task_schema.jsonify(new_task)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route("/tasks/<id>", methods=["GET"])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

if __name__ == "__main__":
    app.run(debug=True)
