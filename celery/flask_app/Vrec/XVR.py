# utils.py 
import time
import logging
import requests
#from   BDB_dbClass     import BDBDatabase

from   Vrec.VRecCamera      import ProcessVideoList
from   Vrec.VRecWSClient    import VRecWSClient
from   Vrec.BDB_dbClass     import BDBDatabase



class XVR():
    def __init__(self) -> None:
        count = 0
        self.bdb = BDBDatabase()
        self.XVRIP = self.bdb.GetVRecIP()
        #self.XVRIP = self.bdb.GetXVRIP()
        
    def update_sucursal_cameras_status(self,sucursal):
        #logging.info(f"ProcessXVR.update_sucursal_cameras ({sucursal})")
        numeroSuc = sucursal[0]
        vrecHost  = sucursal[1]
        vrecPost  = sucursal[2]
        logging.info(f"Procesando Sucursal: {numeroSuc} {sucursal}")    
        vrec = VRecWSClient(vrecHost, port=vrecPost, sucursal=numeroSuc)
        if (vrec.client): # and numeroSuc == 105):
            cameras = vrec.GetCameraList()
            for cameraId in cameras:
                camera = vrec.GetCameraData(cameraId)
                if camera:
                    camaraInfo = {}
                    camaraInfo['sucursal']       = numeroSuc
                    camaraInfo['camara']         = camera["CameraID"]
                    camaraInfo['status']         = camera["Status"]
                    camaraInfo['enable']         = camera["Enable"]
                    self.bdb.UpdateCameraStatus(camaraInfo)

        return "Terminado"

    def update_sucursal_cameras(self,sucursal):
        logging.info(f"ProcessXVR.update_sucursal_cameras ({sucursal})")
        numeroSuc = sucursal[0]
        vrecHost  = sucursal[1]
        vrecPost  = sucursal[2]
        logging.info(f" Procesando Sucursal: {numeroSuc} {sucursal}")  
        self.bdb.WriteLog(numeroSuc, "Started")

        vrec = VRecWSClient(vrecHost, port=vrecPost, sucursal=numeroSuc)

        if (vrec.exception):
            self.bdb.WriteLog(numeroSuc, vrec.exception)
            self.bdb.UpdateStatus(numeroSuc, vrec.exception)
        else:
            self.bdb.UpdateStatus(numeroSuc, "Online")
        
        if (vrec.client and not vrec.exception): # and numeroSuc == 105):
            self.bdb.WriteLog(numeroSuc, "CameraList")        
            cameras = vrec.GetCameraList()
            for cameraId in cameras:
                self.bdb.WriteLog(numeroSuc, f"CameraId:{cameraId}")

                camera = vrec.GetCameraData(cameraId)
                videoList = vrec.GetCameraVideoList(cameraId)
                if (videoList):
                    self.bdb.WriteLog(numeroSuc, f"VideoListt:{cameraId}")

                    #print("VideoList: ", videoList)
                    firstDate, lastDate, lost = ProcessVideoList(videoList)

                    camaraInfo = {}
                    camaraInfo['sucursal']       = numeroSuc
                    camaraInfo['camara']         = camera["CameraID"]
                    camaraInfo['nombre']         = camera["Name"]
                    camaraInfo['host']           = camera["Host"]
                    camaraInfo['port']           = camera["PortHTTP"]
                    camaraInfo['sdk']            = camera["SDK"]
                    camaraInfo['user']           = camera["User"]
                    camaraInfo['password']       = camera["Password"]
                    camaraInfo['fps']            = camera["FrameRate"]
                    camaraInfo['status']         = camera["Status"]
                    camaraInfo['enable']         = camera["Enable"]
                    camaraInfo['recycle_mode']   = camera["RecycleMode"]
                    camaraInfo['recycle_status'] = camera["RecycleStatus"]
                    camaraInfo['firstDate']      = str(firstDate)
                    camaraInfo['lastDate']       = str(lastDate)
                    camaraInfo['lost']           = lost

                    file = open('logslost22.txt','a+')  
                    if lost:
                        for lost_segment in lost:
                            logging.info(f"Lost(): {camaraInfo['sucursal'] , camaraInfo['camara'] ,lost_segment } ")
                            if len(lost_segment) == 2:
                                #queryStr = f"INSERT INTO camara_video_lost VALUES({camaraInfo['sucursal']}, {camaraInfo['camara']}, '{lost_segment[0]}'," \
                                #        f"'{lost_segment[1]}','{0}', '2022-12-07 10:00:09')"
                                print(lost_segment)
                                file.write("\n")
                                file.write(f"video_lost {camaraInfo['sucursal']} {camaraInfo['camara']} - {lost_segment[0]} {lost_segment[1]} ")
                    self.bdb.UpdateCameraRecord(camaraInfo)
                    self.bdb.UpdateCameraLost(camaraInfo, lost)
        try:
            vrec = None
            self.bdb.WriteLog(numeroSuc, "Finished")
            return f"Terminando Sucursal: {numeroSuc}:'{vrecHost}'"
        except:
            self.bdb.WriteLog(numeroSuc, "Exception")
            return "EXCEPTION"
        #return "Terminado"

    def truncate_table(self,table):
        logging.info(f"ProcessXVR.truncate_table ({table})")
        self.bdb.TruncateTable(table)
        return "Truncado"




