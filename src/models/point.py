from utils.connection import Database

class PointModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def post_one_point(self, id_nodo, id_route):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO point (id_nodo, id_route) VALUES (%s, %s);"
      cursor.execute(sql, (id_nodo, id_route))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      print(f"Error {e}")

  def get_by_id_route(self, id_route):
    cursor = self.db.cursor()
    try:
      sql = "SELECT n.latitud, n.longitud, n.id_nodo FROM point p JOIN nodo n ON n.id_nodo = p.id_nodo WHERE id_route = %s;"
      cursor.execute(sql, (id_route,))
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      print(f"Error {e}")