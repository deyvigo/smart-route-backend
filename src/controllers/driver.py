from models import PointModel, RouteModel

class DriverController:
  @staticmethod
  def get_id_route(id_driver):
    if not id_driver:
      return { "Error": "no se ha enviado ninguna id" }, 400
    route_data = RouteModel().get_by_id_driver(id_driver)[0].get("data")

    if not route_data:
      return { "Error": "no existen rutas para este conductor" }, 404

    # accede al primer elemento guardado en bd y saca el id_route
    route = route_data[0]

    response = {}

    response["route"] = route

    point_route = PointModel().get_by_id_route(route["id_route"])[0].get("data")
    
    response["points"] = point_route

    return { "data": response }