#!/usr/bin/env python3
import mysql.connector
import pandas as pd
import logging
from   mysql.connector import errorcode
from   multiprocessing import Lock
from   datetime import datetime


ELIPGO_DDNSDomain = 'elipgodns.com'
DB_Host           = '10.200.3.80'
DB_Database       = 'bdb'
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


    def GetXVRIP(self):
        logging.info(f"GetXVRIP()")

        # Lectura de los registros de la table "direccionamiento" Sitios Fase 2
        self.lock.acquire()
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT sucursal, xvr, xvr_port, xvr_user, xvr_password FROM vXVRIP where fase = 2")
        myresult = mycursor.fetchall()
        columns  = mycursor.description
        mycursor.close()
        self.lock.release()

        return(myresult)


    def GetVRecIP(self):
        logging.info(f"GetVFRecIP()")

        # Lectura de los registros de la table "direccionamiento" Sitios Fase 1
        self.lock.acquire()
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT sucursal, xvr, xvr_port, xvr_user, xvr_password FROM vXVRIP where fase = 1")
        myresult = mycursor.fetchall()
        columns  = mycursor.description
        mycursor.close()
        self.lock.release()

        return(myresult)        


    def UpdateStatus(self, sucursal, status):
        logging.info(f"WriteStatus({sucursal}, '{status}')")

        queryStr = f"UPDATE sucursal SET status='{status}', lastUpdate='{datetime.now()}' WHERE sucursal = {sucursal}"

        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
        except:
            pass
        self.lock.release()


        # Actualiza el estatus del 
    def ReadCameraRecord(self, sucursal, camera):
        logging.info(f"ReadCameraRecord({sucursal},{camera})")

        queryStr = f"SELECT * FROM camara WHERE sucursal={sucursal} AND camara={camera}"
        try:
            self.lock.acquire()            
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            myresult = mycursor.fetchall()
            mycursor.close()
            self.lock.release()
            return myresult
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.lock.release()


    def UpdateCameraStatus(self, cameraInfo):
        logging.info(f"UpdateCameraStatus()")
        #print(cameraInfo)
        record = self.ReadCameraRecord(cameraInfo['sucursal'], cameraInfo['camara'])
        if record:
            #print("Existe, se debe actualizar")
            queryStr = f"UPDATE camara SET status='{cameraInfo['status']}', enable='{cameraInfo['enable']}' " \
                       f"WHERE sucursal={cameraInfo['sucursal']} and camara={cameraInfo['camara']}"

        #print(queryStr)
        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
        except:
            pass
            self.lock.release()

    def TruncateTable(self, table):
        logging.info(f"TruncateTable()")
        queryStr = f"TRUNCATE table {table}" 
        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
        except:
            pass
            self.lock.release()

    def UpdateCameraLost(self, cameraInfo, lost):
        logging.info(f"UpdateCameraLost()")
        #print(cameraInfo)
        if lost:
            for lost_segment in lost:
                logging.info(f"Lost(): {cameraInfo['sucursal'] , cameraInfo['camara'] ,lost_segment } ")


                if len(lost_segment) == 2:
                    queryStr = f"INSERT INTO camara_video_lost VALUES({cameraInfo['sucursal']}, {cameraInfo['camara']}, '{lost_segment[0]}'," \
                            f"'{lost_segment[1]}','{0}','{datetime.now()}')"

                    
                    #Buscar si existe el elemento
                    query1=f"SELECT * from camara_video_lost where sucursal={cameraInfo['sucursal']} and camara={cameraInfo['camara']} and segmento_inicio='{lost_segment[0]}' and segmento_fin='{lost_segment[1]}'"
                    #print(queryStr)
                    myresult=None
                    try:
                        self.lock.acquire()
                        mycursor = self.connection.cursor()
                        mycursor.execute(query1)
                        myresult = mycursor.fetchall()
                        mycursor.close()
                        self.lock.release()
                    except:
                        pass

                    if myresult:
                        logging.info(f"YaExisteElRegistro(): {myresult} ")
                        logging.info(f"YaExisteElRegistro(): {myresult} ")
                    else:
                        logging.info(f"\n\n\nNoExisteElRegistro(): CreandoNuevoRegistro\n\n\n ")
                        #if len(lost_segment) == 2:
                        #    queryStr = f"INSERT INTO camara_video_lost VALUES({cameraInfo['sucursal']}, {cameraInfo['camara']}, '{lost_segment[0]}'," \
                        #            f"'{lost_segment[1]}','{0}', '2022-12-07 10:00:09')"
                        
                        #logging.info(f"Insertar:({queryStr})")

                        if 1:
                            self.lock.acquire()
                            mycursor = self.connection.cursor()
                            mycursor.execute(queryStr)
                            self.connection.commit()
                            mycursor.close()
                            self.lock.release()
                        else:
                            logging.warning(f"Error adding CameraLost()")
                            pass
                            self.lock.release()
           



    def UpdateCameraRecord(self, cameraInfo):
        logging.info(f"UpdateCameraRecord()")
        #print(cameraInfo)
        
        record = self.ReadCameraRecord(cameraInfo['sucursal'], cameraInfo['camara'])
        if not record:
            #print("No existe, se debe crear")
            queryStr = f"INSERT INTO camara VALUES({cameraInfo['sucursal']}, {cameraInfo['camara']}, '{cameraInfo['nombre']}'," \
                       f"'{cameraInfo['host']}',{cameraInfo['port']},'{cameraInfo['sdk']}','{cameraInfo['user']}',"             \
                       f"'{cameraInfo['password']}',{cameraInfo['fps']},'{cameraInfo['status']}','{cameraInfo['enable']}',"     \
                       f"'{cameraInfo['recycle_mode']}','{cameraInfo['recycle_status']}','{cameraInfo['firstDate']}',"          \
                       f"'{cameraInfo['lastDate']}','{datetime.now()}')"
        else:
            #print("Existe, se debe actualizar")
            queryStr = f"UPDATE camara SET status='{cameraInfo['status']}', enable='{cameraInfo['enable']}', " \
                       f"first_video='{cameraInfo['firstDate']}', last_video='{cameraInfo['lastDate']}' "      \
                       f"WHERE sucursal={cameraInfo['sucursal']} and camara={cameraInfo['camara']}"

        #print(queryStr)
        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
        except:
            pass
            self.lock.release()


    def WriteLog(self, sucursal, estatus):
        logging.info(f"WriteLog({sucursal},'{estatus}')")

        queryStr = f"INSERT INTO process_log VALUES ({sucursal}, '{estatus}', '{datetime.now()}')"
        #print(queryStr)

        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
        except mysql.connector.Error as err:
            print(f"WriteLog Exception: {err}")
            self.lock.release()
