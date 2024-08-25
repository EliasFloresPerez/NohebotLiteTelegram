import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()

class BaseDeDatosJson:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_DATABASE")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = os.getenv("DB_PORT")
        self.connection = None
        self.cursor = None

    
        

    # Método para abrir la conexión
    def abrir_conexion(self):
        
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
                self.cursor = self.connection.cursor()
                print("Conexión a la base de datos abierta.")
                self.crear_tabla()
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Error al conectarse a la base de datos: {error}")
    
    # Método para cerrar la conexión
    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("Conexión a la base de datos cerrada.")
    
    # Método para crear la tabla
    def crear_tabla(self):
        try:
            self.abrir_conexion()  # Aseguramos que la conexión esté abierta
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS estado (
                    id SERIAL PRIMARY KEY,
                    Tareas TEXT NOT NULL
                );
            """)
            self.connection.commit()
            

            self.insertar_tareas("{}")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error al crear la tabla: {error}")
    
    # Método para insertar un string en la columna Tareas (solo permite un registro)
    def insertar_tareas(self, contenido):
        try:
            # Verificar si ya existe un registro en la tabla
            self.cursor.execute("SELECT COUNT(*) FROM estado;")
            count = self.cursor.fetchone()[0]
            
            if count > 0:
                pass
            else:
                self.cursor.execute("INSERT INTO estado (Tareas) VALUES (%s) RETURNING id;", (contenido,))
                self.connection.commit()
                return self.cursor.fetchone()[0]  # Devuelve el id del registro insertado
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error al insertar las tareas: {error}")
    
    # Método para obtener las tareas por id
    def obtener_tareas(self, id):
        try:
            self.cursor.execute("SELECT Tareas FROM estado WHERE id = %s;", (id,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado[0]  # Devuelve el contenido de la fila con ese id
            else:
                return None  
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error al obtener las tareas: {error}")
    
    # Método para modificar las tareas por id
    def modificar_tareas(self, id, nuevo_contenido):
        try:
            self.cursor.execute("UPDATE estado SET Tareas = %s WHERE id = %s;", (nuevo_contenido, id))
            self.connection.commit()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error al modificar las tareas: {error}")
    
    # Método para eliminar tareas por id
    def eliminar_tareas(self, id):
        try:
            self.cursor.execute("DELETE FROM estado WHERE id = %s;", (id,))
            self.connection.commit()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error al eliminar las tareas: {error}")


