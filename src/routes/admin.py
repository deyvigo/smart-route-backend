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

@admin_blueprint.route("/admin/rand", methods=["GET"])
def rand_client():
  return AdminController.rand_clients()