#!/usr/bin/env python3
from   requests        import Session
from   requests.auth   import HTTPBasicAuth
from   zeep            import Client
from   zeep.transports import Transport
from   zeep.cache      import SqliteCache
from   icmplib         import ping
from   contextlib      import closing
import json
import zeep
import logging
import socket
import ipaddress
import requests


DEFAULT_PORT     = 80
DEFAULT_USER     = "root"
DEFAULT_PASSWORD = "root"
PING_COUNT         = 4
PING_TIMEOUT       = 2
PING_INTERVAL      = 0.2


class VRecWSClient():
    # Inicialización de Instancia
    def __init__(self, host, port=DEFAULT_PORT, user=DEFAULT_PASSWORD, password=DEFAULT_PASSWORD, sucursal=0):
        self.host      = host
        self.port      = port 
        self.user      = user
        self.password  = password
        self.client    = None
        self.exception = ""

        # Checa si el Puerto es accesible
        if (self.CheckPort()):
            # Estable la URL
            self.url = f"http://{self.host}:{self.port}/WebServiceConfigurationVMonitoring/WebServiceConfiguration.asmx?wsdl"

            # Inicia la Sesion con autenticación básica
            self.session      = Session()
            self.session.auth = HTTPBasicAuth(self.user, self.password)

            try:            
                #transport   = Transport(session=self.session, timeout=10)
                cache       = SqliteCache(path='/tmp/sqlite.db', timeout=60)
                transport   = Transport(session=self.session, cache=cache, timeout=15)#, max_retries=3)
                print("URL:", self.url)
                self.client = Client(self.url, transport=transport)
                self.client.settings(strict=False)
                
                if (self.client):
                    #print(f"Antes login: {self.user}/{self.password}")
                    response = self.client.service.loginSystemTimeOut(self.user, self.password, 15)
                    #print(response)
                    #print(self.client)  
            except:
                print(f"Excepción - Sucursal: {sucursal}")
                self.exception = "Excepcion"
            #except zeep.exceptions.Fault as fault:
            #    print("FAULT:", fault, fault.detail)
            #except (requests.exceptions.HTTPError, KeyError, TimeoutError) as e:
            #    print(e.message)
            #    self.exception = "Excepcion"
            #    print(f"Excepción - Sucursal: {sucursal}")
        else:
            self.exception = "Sin Acceso"
            print(f"No accesible: '{self.host}:{self.port}'")


    def Ping(self, count=PING_COUNT, timeout=PING_TIMEOUT, interval=PING_INTERVAL):
        logging.info(f"Ping({self.host})")

        print(self.host)
        hostRsp    = ping(self.host, count, timeout, interval)
        print(hostRsp)
        self.ping  = hostRsp
        try:
            self.ip_address = socket.gethostbyname(self.url) 
        except:
            self.ip_address = ""
        return hostRsp.is_alive


    def CheckPort(self):
        logging.info(f"CheckPort('{self.host}',{self.port})")

        host = ""
        try:
            ipaddress.ip_network(self.host)
            host = self.host
        except:
            try:
                host = socket.gethostbyname(self.host)
            except:
                return False

        socket.setdefaulttimeout(30)
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if (sock.connect_ex((host, self.port)) == 0):
                print("Port is open")
                return True
            else:
                print("Port is not open")
                return False


    # Obtiene la información de los Repositorios
    def GetRepositories(self):
        logging.info(f"GetRepositories()")

        response = self.client.service.SystemConfiguration_GetRepositoryList()

        if (response['SystemConfiguration_GetRepositoryListResult'] == 'OK'):
            self.repositories = response['repositoryConfigList']['RepositoryConfig']
        print(self.repositories)


    def GetBackupRepository(self):
        logging.info(f"GetBackupRepository()")

        response = self.client.service.SystemConfiguration_GetRepositoryBackupList()
        if (response['SystemConfiguration_GetRepositoryBackupListResult'] == 'OK'):
            self.backupRepository = response['repositoryConfigList']['RepositoryBackupConfig']
        print(self.backupRepository)


    def GetCameraList(self):
        logging.info(f"GetCameraList()")
        
        response = self.client.service.CameraConfiguration_GetCameraList()
        #print(str(response))

        if (response['CameraConfiguration_GetCameraListResult'] == 'OK'):
            if (response['cameraIDList']):
                self.cameraList = response['cameraIDList']['string']
                #print(self.cameraList)
                return self.cameraList


    def GetCameraData(self, camera):
        logging.info(f"GetCameraData({camera})")

        response = self.client.service.CameraConfiguration_GetCameraData(camera)
        if (response['CameraConfiguration_GetCameraDataResult'] == 'OK'):
            #print(response['cameraConfig'])
            return(response['cameraConfig'])


    # 
    # Obtiene la lista de videos disponibles (fehca y hora) de la cámara 
    #
    def GetCameraVideoList(self, camera):
        #logging.info(f"GetCamera({camera})")
        logging.info(f"GetCameraVideoList_({camera})")
        #return None
        response = self.client.service.FileSystem_GetVideoList(camera)
        #print(response)
        if (response['FileSystem_GetVideoListResult'] == 'OK'):
            if (response['videoList']):
                #print(response['videoList']['string'])
                return(response['videoList']['string'])
        
        return None
