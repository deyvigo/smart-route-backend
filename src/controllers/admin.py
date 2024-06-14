from models import AdminModel, DriverModel
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
  
  @staticmethod
  def create_one_driver():
    created_by = request.json.get("created_by")

    admin = AdminModel().get_by_username(created_by).get("data")
    if not admin:
      return { "Error": "admin username no existe" }
    
    username = request.json.get("username")

    driver = DriverModel().get_by_username(username).get("data")
    if driver:
      return { "Error": "username ya existe" }

    default_status = "inactivo"
    password = request.json.get("password")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    hashed_pass = bcrypt.generate_password_hash(password)

    response = DriverModel().post_one_driver(username, password, first_name, last_name, default_status, admin["id_admin"])

    if response:
      return response
    return { "Error": "no se pudo crear al driver" }
  
  @staticmethod
  def update_status_by_driver():
    username = request.json.get("username")
    status = request.json.get("status")

    response = DriverModel().update_status_by_username(status, username)

    if response["row_count"] > 0:
      return response
    return { "Error": "no se actualizo el estado de ningun driver" }