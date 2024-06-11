import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".envvars")

class Database:
  def __init__(self):
    db = self.connection()
    try:
      cursor = db.cursor()
      cursor.execute("SHOW TABLES;")
      db_tables = cursor.fetchall()
      if (db_tables.__len__() > 0):
        print("Las tablas ya están creadas.")
      else:
        self.create_tables()
    except Exception as e:
      print(f"Error durante la creación de las tablas: {e}")

  def create_tables(self):
    db = self.connection()
    try:
      cursor = db.cursor()
      cursor.execute("""
        create table if not exists nodo
        (
          id       bigint    not null
            primary key,
          latitud  double not null,
          longitud double not null
        );
      """)

      cursor.execute("""
        create table if not exists arista
        (
          id_arista bigint auto_increment
            primary key,
          distancia double not null,
          origen    bigint    not null,
          destino   bigint    not null,
          constraint arista_nodo_id_fk
            foreign key (origen) references nodo (id),
          constraint arista_nodo_id_fk_2
            foreign key (destino) references nodo (id)
        );
      """)
    except Exception as e:
      print(f"Error durante la creaciónd de tablas. {e}")

  def connection(self):
    db = pymysql.connections.Connection(
      host=os.getenv("DATABASE_HOST"),
      database=os.getenv("DATABASE_NAME"),
      user=os.getenv("DATABASE_USER"),
      password=os.getenv("DATABASE_PASSWORD"),
      port=3306,
      cursorclass=pymysql.cursors.DictCursor
    )
    return db