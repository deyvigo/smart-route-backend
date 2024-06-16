from models import AdminModel, DriverModel
from flask_jwt_extended import create_access_token

from flask import request
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class LoginController:
  @staticmethod
  def login_admin():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
      return { "Error": "no ingreso los datos necesarios" }, 400
    
    user_on_bd = AdminModel().get_by_username(username)["data"]

    if not user_on_bd:
      return { "error": "el usuario no existe" }, 404
    
    if bcrypt.check_password_hash(user_on_bd["password"], password):
      acces_token = create_access_token(identity={
        "username": username,
        "id_admin": user_on_bd["id_admin"],
        "role": "ROLE_ADMIN"
      })
      return { "token": acces_token }, 200
    else:
      return { "error": "contraseña incorrecta" }, 401
    
  @staticmethod
  def login_driver():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
      return { "Error": "no ingreso los datos necesarios" }, 400
    
    user_on_bd = DriverModel().get_by_username(username)["data"]

    if not user_on_bd:
      return { "error": "el usuario no existe" }, 404
    
    if bcrypt.check_password_hash(user_on_bd["password"], password):
      acces_token = create_access_token(identity={
        "username": username,
        "id_driver": user_on_bd["id_driver"],
        "role": "ROLE_DRIVER"
      })
      return { "token": acces_token }, 200
    else:
      return { "error": "contraseña incorrecta" }, 401