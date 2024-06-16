from flask import Blueprint
from controllers import DriverController

driver_blueprint = Blueprint("driver", __name__)

@driver_blueprint.route("/driver/route/<id_driver>", methods=["GET"])
def get_route(id_driver):
  return DriverController.get_id_route(id_driver)