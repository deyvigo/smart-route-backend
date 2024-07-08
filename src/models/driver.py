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

  # for login driver
  def get_by_username(self, username):
    cursor = self.db.cursor()
    try:
      query = "SELECT * FROM driver WHERE BINARY username = %s;"
      cursor.execute(query, (username,))
      response = cursor.fetchone()
      return { "data": response }
    except Exception as e:
      print(f"Error {e}")

  def get_by_id_without_password(self, id_driver):
    cursor = self.db.cursor()
    try:
      query = "SELECT id_driver, created_by, username, first_name, last_name, status FROM driver WHERE id_driver = %s;"
      cursor.execute(query, (id_driver,))
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      print(f"Error {e}")

  def get_all_without_password(self):
    cursor = self.db.cursor()
    try:
      query = "SELECT id_driver, created_by, username, first_name, last_name, status FROM driver;"
      cursor.execute(query)
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      print(f"Error {e}")

  def update_status_by_username(self, status, username):
    cursor = self.db.cursor()
    try:
      query = "UPDATE driver SET status = %s WHERE username = %s;"
      cursor.execute(query, (status, username))
      self.db.commit()
      return { "row_count": cursor.rowcount }
    except Exception as e:
      print(f"Error {e}")

  def get_all_actives_status(self):
    cursor = self.db.cursor()
    try:
      query = "SELECT * FROM driver WHERE status = 'activo';"
      cursor.execute(query)
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      print(f"Error {e}")

  def delete_by_id(self, id_driver):
    cursor = self.db.cursor()
    try:
      query = "DELETE FROM driver WHERE id_driver = %s;"
      cursor.execute(query, (id_driver,))
      self.db.commit()
      if cursor.rowcount == 0:
        return { "error": "Registro no encontrado" }, 404
      else:
        return { "message": "Registro eliminado exitosamente" }, 200
    
    except Exception as e:
      print(f"Error {e}")