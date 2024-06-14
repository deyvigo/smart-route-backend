from flask import Blueprint
from controllers import AdminController

admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/admin/register", methods=["POST"])
def register_admin():
  return AdminController.create_one_admin()