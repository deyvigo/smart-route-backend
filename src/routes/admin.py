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