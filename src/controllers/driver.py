from models import PointModel, RouteModel, DriverModel

class DriverController:
  @staticmethod
  def get_route_by_id_driver(id_driver):
    if not id_driver:
      return { "error": "no se ha enviado ninguna id" }, 400
    route_data = RouteModel().get_by_id_driver(id_driver)[0].get("data")

    if not route_data:
      return { "error": "no existen rutas para este conductor" }, 404

    # accede al primer elemento guardado en bd
    route = route_data[0]

    response = {}

    response["route"] = route

    point_route = PointModel().get_by_id_route(route["id_route"])[0].get("data")
    
    response["route"]["points"] = point_route

    return { "data": response }
  
  def get_info_by_id(id_driver):
    response = DriverModel().get_by_id_without_password(id_driver)
    if response[0]["data"]:
      return response
    return { "error": "No se pudo obtener la informacion del conductor" }, 404