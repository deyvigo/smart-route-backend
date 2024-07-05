from flask import Blueprint
from controllers import AdminController

admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/admin/register", methods=["POST"])
def register_admin():
  return AdminController.create_one_admin()

@admin_blueprint.route("/admin/register/driver", methods=["POST"])
def regist_one_driver():
  return AdminController.create_one_driver()

@admin_blueprint.route("/admin/update/driver/status", methods=["PUT"])
def update_status_from_driver():
  return AdminController.update_status_by_driver()

@admin_blueprint.route("/admin/create/clients", methods=["POST"])
def create_clients():
  return AdminController.create_clients()

# @admin_blueprint.route("/admin/randomize", methods=["GET"])
# def randomize_routes():
#   return AdminController.randomize()

@admin_blueprint.route("/admin/rand/old", methods=["GET"])
def rand_client():
  return AdminController.rand_clients()

@admin_blueprint.route("/admin/all/drivers", methods=["GET"])
def get_all_drivers():
  return AdminController.get_all_drivers()

@admin_blueprint.route("/admin/all/clients", methods=["GET"])
def get_all_clients():
  return AdminController.get_all_clients()

@admin_blueprint.route("/admin/delete/driver/<id_driver>", methods=["DELETE"])
def delete_driver_by_id(id_driver):
  return AdminController.delete_driver_by_id(id_driver)

@admin_blueprint.route("/admin/all/routes", methods=["GET"])
def get_all_routes():
  return AdminController.get_all_routes()

@admin_blueprint.route("/admin/info/<id_admin>", methods=["GET"])
def get_info_by_id(id_admin):
  return AdminController.get_info_admin_by_id(id_admin)

@admin_blueprint.route("/admin/rand", methods=["GET"])
def rand():
  return AdminController.rand()