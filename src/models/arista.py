from utils.connection import Database

class ModelArista:
  def __init__(self):
    self.db = Database().connection()

  def __del__(self):
    if self.db:
      self.db.close()

  def post_one_nodo(self, origen, destino, distancia):
    cursor = self.db.cursor()
    try:
      query = "INSERT INTO arista (origen, destino, distancia) VALUES (%s, %s, %s);"
      cursor.execute(query, (origen, destino, distancia))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      print(f"Error {e}")
  
  def get_all_arists(self):
    cursor = self.db.cursor()
    try:
      cursor.execute("SELECT * FROM arista;")
      response = cursor.fetchall()
      return { "data": response }
    except:
      return { "error": "Error durante la consulta a la tabla nodo."}