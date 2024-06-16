from utils.connection import Database

class RouteModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def post_one_route(self, total_distance, id_driver):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO route (total_distance, id_driver) VALUES (%s, %s);"
      cursor.execute(sql, (total_distance, id_driver))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      print(f"Error {e}")

  def get_by_id_driver(self, id_driver):
    cursor = self.db.cursor()
    try:
      sql = "SELECT id_route, total_distance FROM route WHERE id_driver = %s;"
      cursor.execute(sql, (id_driver,))
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      print(f"Error {e}")