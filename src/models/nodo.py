from utils.connection import Database

class ModelNodo:
  def __init__(self):
    self.db = Database().connection()

  def __del__(self):
    if self.db:
      self.db.close()

  def post_one_nodo(self, id, latitud, longitud):
    cursor = self.db.cursor()
    try:
      query = "INSERT INTO nodo (id, latitud, longitud) VALUES (%s, %s, %s);"
      cursor.execute(query, (id, latitud, longitud))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      print(f"Error {e}")
  
  def get_all_nodo(self):
    cursor = self.db.cursor()
    try:
      cursor.execute("SELECT * FROM nodo;")
      response = cursor.fetchall()
      return { "data": response }
    except:
      return { "error": "Error durante la consulta a la tabla nodo."}