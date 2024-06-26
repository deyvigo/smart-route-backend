from utils.connection import Database

class ClientModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def post_one_client(self, name, latitud, longitud):
    cursor = self.db.cursor()
    try:
      query = "INSERT INTO client (name, latitud, longitud) VALUES (%s, %s, %s);"
      cursor.execute(query, (name, latitud, longitud))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }
    except Exception as e:
      print(f"Error {e}")

  def get_all_clients(self):
    cursor = self.db.cursor()
    try:
      query = "SELECT id_client, name, latitud, longitud FROM client;"
      cursor.execute(query)
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      print(f"Error {e}")