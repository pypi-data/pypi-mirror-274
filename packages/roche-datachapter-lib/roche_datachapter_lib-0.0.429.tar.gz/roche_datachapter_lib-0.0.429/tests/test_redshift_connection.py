import os
from sqlalchemy import create_engine

# Cargar las variables de entorno
USER = os.getenv('RDI_LATAM_AR_USER')
PASSWORD = os.getenv('RDI_LATAM_AR_PASSWORD')
HOST = os.getenv('RDI_LATAM_AR_HOST')
PORT = os.getenv('RDI_LATAM_AR_PORT')
DB = os.getenv('RDI_LATAM_AR_DB')

# Crear la cadena de conexión con sslmode deshabilitado
connection_string = f'redshift+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}?sslmode=disable'

# Crear el motor de SQLAlchemy
engine = create_engine(connection_string)

# Probar la conexión (opcional)
try:
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM gtm_latam_arg.stg_oceo.oceo_omuser_latest")
        for row in result:
            print(row)
except Exception as e:
    print(f"Error connecting to the database: {e}")
