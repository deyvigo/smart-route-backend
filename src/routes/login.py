from flask import Blueprint
from controllers import LoginController

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route("/login/admin", methods=["POST"])
def login_admin():
  return LoginController.login_admin()

@login_blueprint.route("/login/driver", methods=["POST"])
def login_driver():
  return LoginController.login_driver()