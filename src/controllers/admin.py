from models import AdminModel
from flask import request
from flask_bcrypt import  Bcrypt

bcrypt = Bcrypt()

class AdminController:
  @staticmethod
  def create_one_admin():
    username = request.json.get("username")
    password = request.json.get("password")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    hashed_pass = bcrypt.generate_password_hash(password)
    response = AdminModel().post_one_admin(username, hashed_pass, first_name, last_name)
    if response:
      return { "Exito": "Admin agregado" }
    return { "Error": "No se pudo registrar" }
