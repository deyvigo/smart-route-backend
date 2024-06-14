from utils.connection import Database

class ClientExactModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def post_one_client_exact(self, id_client, id_nodo):
    cursor = self.db.cursor()
    try:
      query = "INSERT INTO client_exact (id_client, id_nodo) VALUES (%s, %s);"
      cursor.execute(query, (id_client, id_nodo))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }
    except Exception as e:
      print(f"Error {e} from table client_exact")