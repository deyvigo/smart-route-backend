from utils.connection import Database

class DriverModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def post_one_driver(self, username, password, first_name, last_name, status, created_by):
    cursor = self.db.cursor()
    try:
      query = "INSERT INTO driver (username, password, first_name, last_name, status, created_by) VALUES (%s, %s, %s, %s, %s, %s);"
      cursor.execute(query, (username, password, first_name, last_name, status, created_by))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      print(f"Error {e}")

  def get_by_username(self, username):
    cursor = self.db.cursor()
    try:
      query = "SELECT * FROM driver WHERE username = %s;"
      cursor.execute(query, (username,))
      response = cursor.fetchone()
      return { "data": response }
    except Exception as e:
      print(f"Error {e}")

  def get_all(self):
    cursor = self.db.cursor()
    try:
      query = "SELECT * FROM driver;"
      cursor.execute(query)
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      print(f"Error {e}")