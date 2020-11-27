import datetime
from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, User

## Nos permite encriptar y desencriptar nuestras contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite definir configuraciones de consultas o peticiones (request) 
from flask_cors import CORS

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity

## Nos permite leer de un archivo .env
from dotenv import load_dotenv
from os import access, environ
load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
    environ.get('DBUSER'), 
    environ.get('DBPASS'), 
    environ.get('DBHOST'), 
    environ.get('DBPORT'),
    environ.get('DBNAME')
)
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
db.init_app(app)
jwt = JWTManager(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username:
            return jsonify({"msg": "Username is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"msg": "Username  already exists"}), 400

        user = User()
        user.username = username
        user.password = generate_password_hash(password)
        user.save()

        return jsonify({"success": "Thanks. your register was successfully"})

@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username:
            return jsonify({"msg": "Username is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        expires = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.username, expires_delta=expires)

        data = {
            "access_token": access_token,
            "user": user.serialize(),
            "expires_at": expires.total_seconds()*1000
        }

        return jsonify(data), 200

@app.route('/api/profile', methods=['GET'])
@jwt_required
def profile():
    if request.method == 'GET':
        username = get_jwt_identity()
        return jsonify({"success": "Acceso a espacio privado", "username": username}), 200

if __name__ == '__main__':
    manager.run()