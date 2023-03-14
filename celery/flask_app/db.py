import mysql.connector
import logging
from   mysql.connector import errorcode
from   multiprocessing import Lock

ELIPGO_DDNSDomain = 'elipgodns.com'
DB_Host           = '10.200.3.80'
DB_Database       = 'viva'
DB_User           = 'elipgo'
DB_Password       = '3l1pg0$123'

#
# Clase de la base de datos
#
class BDBDatabase:
    # Inicialización y conección a la Base de Datos
    def __init__(self, host = DB_Host, database = DB_Database, user = DB_User, password = DB_Password):
        #print("ElipgoDB Constructor(%s)" % (database))
        # Asigna variables de la clase
        self.host       = host
        self.database   = database
        self.user       = user
        self.password   = password
        self.lock       = Lock()

        try:
            self.connection = mysql.connector.connect(user      = self.user,
                                                      password  = self.password,
                                                      host      = self.host,
                                                      database  = self.database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Algo esta mal con el Usuario y Password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de datos no existe.")
            else:
                print(err)

    def GetSitios(self):
        logging.info(f"GetSitios()")
        # Lectura de los Sitios 
        self.lock.acquire()
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT proyecto,sitio,ip,status,is_alive,last_update FROM sitio where proyecto='MC'")
        myresult = mycursor.fetchall()
        columns  = mycursor.description
        mycursor.close()
        self.lock.release()
        return(myresult)   