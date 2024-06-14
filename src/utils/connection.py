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
        create table if not exists admin
        (
          id_admin   int auto_increment
            primary key,
          username   varchar(30) not null,
          password   varchar(70) not null,
          first_name varchar(50) not null,
          last_name  varchar(50) not null
        );
      """)

      cursor.execute("""
        create table if not exists client
        (
          id_client int auto_increment
            primary key,
          name      varchar(50) not null,
          latitud   double      not null,
          longitud  double      not null
        );
      """)

      cursor.execute("""
        create table if not exists client_exact
        (
          id_client_exact int auto_increment
            primary key,
          latitud         double not null,
          longitud        double not null,
          id_client       int    null,
          constraint client_exact_client_id_client_fk
            foreign key (id_client) references client (id_client)
        );
      """)

      cursor.execute("""
        create table if not exists driver
        (
          id_driver  int auto_increment
            primary key,
          username   varchar(30) not null,
          password   varchar(70) not null,
          first_name varchar(50) not null,
          last_name  varchar(50) not null,
          status     varchar(20) not null,
          created_by int         not null,
          constraint driver_admin_id_admin_fk
            foreign key (created_by) references admin (id_admin)
        );
      """)

      cursor.execute("""
        create table if not exists driver_client
        (
          id_driver_client int auto_increment
            primary key,
          id_client_exact  int not null,
          id_driver        int not null,
          constraint driver_client_client_exact_id_client_exact_fk
            foreign key (id_client_exact) references client_exact (id_client_exact),
          constraint driver_client_driver_id_driver_fk
            foreign key (id_driver) references driver (id_driver)
        );
      """)

      cursor.execute("""
        create table if not exists nodo
        (
          id_nodo  int    not null
            primary key,
          latitud  double not null,
          longitud double not null
        );
      """)

      cursor.execute("""
        create table if not exists arista
        (
          id_arista int auto_increment
            primary key,
          distancia double not null,
          origen    int    not null,
          destino   int    not null,
          constraint arista_nodo_id_fk
            foreign key (origen) references nodo (id_nodo),
          constraint arista_nodo_id_fk_2
            foreign key (destino) references nodo (id_nodo)
        );
      """)

      cursor.execute("""
        create table if not exists route
        (
          id_route       int auto_increment
            primary key,
          total_distance double not null,
          id_driver      int    not null,
          constraint route_driver_id_driver_fk
            foreign key (id_driver) references driver (id_driver)
        );
      """)

      cursor.execute("""
        create table if not exists point
        (
          id_point int auto_increment
            primary key,
          id_nodo  int not null,
          id_route int null,
          constraint point_nodo_id_fk
            foreign key (id_nodo) references nodo (id_nodo),
          constraint point_route_id_route_fk
            foreign key (id_route) references route (id_route)
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