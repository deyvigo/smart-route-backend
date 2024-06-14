from utils.connection import Database

class AdminModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def post_one_admin(self, username, password, first_name, last_name):
    cursor = self.db.cursor()
    try:
      query = "INSERT INTO admin (username, password, first_name, last_name) VALUES (%s, %s, %s, %s);"
      cursor.execute(query, (username, password, first_name, last_name))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      print(f"Error {e}")


  def get_by_username(self, username):
    cursor = self.db.cursor()
    try:
      query = "SELECT username, password FROM admin WHERE username = %s;"
      cursor.execute(query, (username,))
      response = cursor.fetchone()
      return { "data": response }
    except Exception as e:
      print(f"Error {e}")