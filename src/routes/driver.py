from flask import Blueprint
from controllers import DriverController

driver_blueprint = Blueprint("driver", __name__)

@driver_blueprint.route("/driver/route/<id_driver>", methods=["GET"])
def get_route(id_driver):
  return DriverController.get_route_by_id_driver(id_driver)

@driver_blueprint.route("/driver/info/<id_driver>", methods=["GET"])
def get_info_by_id_driver(id_driver):
  return DriverController.get_info_by_id(id_driver)