from flask import Flask, request
from flask_cors import CORS

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from routes import admin_blueprint, driver_blueprint, login_blueprint, hello_blueprint

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "ada-smart-router"
jwt = JWTManager(app)

bcrypt = Bcrypt(app)
CORS(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(driver_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(hello_blueprint)

@app.route("/helloworld", methods=["GET"])
def hello():
  return { "message": "Hello World" }

if __name__ == "__main__":
  app.run(debug=True)