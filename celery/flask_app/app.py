from flask import Blueprint, render_template, request,redirect,url_for
from flask import Flask
from flask import render_template, request,redirect,url_for
from celery_config import make_celery
from celery.result import ResultSet
from celery.schedules import crontab
import logging
from ping_sites import WEBSITE_LIST
#from sites_combinados import SITES
from sites_micalle import SITES
from status_result_offline import OFFLINE
from sucursales_fase_2 import SUCURSALES
from db import BDBDatabase
import nmap
import subprocess
from requests.adapters import HTTPAdapter

#import commands
import socket
import ipaddress
from   contextlib      import closing

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



from Vrec.XVR import XVR
import os, sys, time
import requests
#from consumer.model.consumer import ConsumerForm

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    #CELERY_BROKER_URL='redis://redis:6379/0',
    #CELERY_RESULT_BACKEND='redis://redis:6379/0'
)

celery = make_celery(app)

celery.conf.task_send_sent_event = True
celery.conf.worker_send_task_events = True

celery.conf.enable_utc = False
celery.conf.update(timezone = 'America/Mexico_City')

celery.conf.beat_schedule = {
#"every-min": {
# "task": "celery.get_status",
# "schedule": 60*240
# },
 "obtener-videos-perdidos-1": {
        "task": "celery.get_sucursales",
        #"schedule": crontab(minute=29, hour=19)
        "schedule": 60*180
    }
,
 "obtener-videos-perdidos-2": {
        "task": "celery.get_sucursales",
        "schedule": crontab(minute=0, hour=18)
    }
}


xvr = XVR()
viva = BDBDatabase()

@app.route('/')
@app.route('/home')
def home():
    return render_template('consumer/consumer_list.html')


@celery.task(name="celery.get_status")
@app.route('/sucursales/status')
def update_sucursal_cameras_status():
    start_time = time.time()
    #print(xvr.XVRIP)
    try:
        rs = ResultSet([update_sucursal_cameras_status_task.delay(address) for address in xvr.XVRIP[:5]])
        # Wait for the tasks to finish 
        rs.get()
    except:
        pass

    end_time = time.time()
    print("CelerySquirrel:", end_time - start_time)
    return str(end_time - start_time)

    
@celery.task(name="celery.get_sucursales")
@app.route('/sucursales')
def update_sucursal_cameras():
    start_time = time.time()
    try:
        #xvr.truncate_table('camara_video_lost')
        rs = ResultSet([update_sucursal_cameras_task.delay(address) for address in xvr.XVRIP])
        rs.get()
    except:
        pass
    end_time = time.time()
    print("CelerySquirrel:", end_time - start_time)
    return str(end_time - start_time)


@celery.task(name="celery.get_sucursal")
@app.route('/sucursal')
def sucursal():
    try:
        for sucursal in xvr.XVRIP:
            if sucursal[0] == 101:
                rs = ResultSet(update_sucursal_cameras_task.delay(sucursal))
                rs.get()
    except:
        pass
    return 'Sucursal procesada'



@celery.task(name="celery.pings")
@app.route('/pings')
def pings():
    start_time = time.time()
    # Using `delay` runs the task async 
    #rs = ResultSet([check_website_task.delay(address) for address in WEBSITE_LIST])
    #WEBSITE_LIST = [
    #    'mc14775.c5cdmx.elipgodns.com',
    #    'mc3988.c5cdmx.elipgodns.com'
    #]
    SITES = viva.GetSitios()
    #for address in SITES:
    #for address in OFFLINE[:1000]:
    print("ABC")
    #print("ABC",SUCURSALES)
    #for address in OFFLINE[:20]:
    for address in SUCURSALES:
    #for address in SITES:
        #address = f"mc{address[1]}.c5cdmx.elipgodns.com"
        print(address)
        #if 'mc' in address:
        if 1:
            check_website_task.delay(address) 
    # Wait for the tasks to finish 
    #rs.get()
    print(len(SITES))
    end_time = time.time()
    print("CelerySquirrel:", end_time - start_time)
    #print(rs)
    return "Finished"


@celery.task(name="celery.update_sucursal_cameras_status_task", time_limit=32)
def update_sucursal_cameras_status_task(sucursal):
    return xvr.update_sucursal_cameras_status(sucursal)

@celery.task(name="celery.update_sucursal_cameras_task", time_limit=120)
def update_sucursal_cameras_task(sucursal):
    return xvr.update_sucursal_cameras(sucursal)




class WebsiteDownException(Exception):
    pass


def ping_website4(host, timeout=10, port=8011):
    logging.info(f"CheckPort('{host}',{port})")
    
    #host = ""
    #if 1:
    #    ipaddress.ip_network(host)
    #    host = host
    #else:
    #    try:
    #        host = socket.gethostbyname(host)
    #    except:
    #        return False

    socket.setdefaulttimeout(30)
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if (sock.connect_ex((host, port)) == 0):
            print("Port is open")
            return 1
        else:
            print("Port is not open")
            return 0



def ping_website(address, timeout=10):
    #response = os.system("ping -c 1 " + address)
    #response = os.system(f"nc -vz {address} 8011 ")
    response=1
    #print(response)
    #for i in range(0,3):
    i="ok"
    if 1:
        nm = nmap.PortScanner()
        r = nm.scan(address, '80', arguments='-Pn  --max-retries 10 --host-timeout 11s')
        try:
            response = nm.all_hosts()[0]
            if response:
                host = nm.all_hosts()[0]
                response = nm[f'{host}'].tcp(80)['state']
                if 'open' in response:
                    print("OPENNN")

            #print("status",nm.scanstats()["uphosts"])
            #print("status port ",nm.scanstats()["uphosts"])
            #print("----->>", response, r)
            #and then check the response...
            #status, output = commands.getstatusoutput("cat /etc/services")
            #comm= f"nmap -p 8011 {address}"
            #print(comm)
            #response = os.popen("nmap -p 8011 mc1.c5cdmx.elipgodns.com").read()
            #print("Response: ",response,type(response))
            print(i,"status:",response)
            if response == "open":
                print (i,address, 'is up!', response)
                return 1
            else:
                print (i,address, 'is down!', response)
                #return 0
        except:
            print (i,address, 'unresolve!', response)
            return -1
    return 0





def ping_website2(address, timeout=10):
    """ 
Check if a website is down. A website is considered down 
if either the status_code >= 400 or if the timeout expires 

Throw a WebsiteDownException if any of the website down conditions are met 
"""
    if 1:
        response = requests.get(address, timeout=timeout)
        logging.warning("response", response)
        #logging.warning("Success  %s returned status_code=%s" % (address, response.status_code))
        if response.status_code >= 400:
            logging.warning("Website %s returned status_code=%s" % (address, response.status_code))
            raise WebsiteDownException()
        else:
            return 1
    else:
    #except requests.exceptions.RequestException:
        logging.warning("Timeout expired for website %s" % address)
        raise WebsiteDownException()
        
def notify_owner(address):
    """ 
Send the owner of the address a notification that their website is down 

For now, we're just going to sleep for 0.5 seconds but this is where 
you would send an email, push notification or text-message 
"""
    logging.info("Notifying the owner of %s website" % address)
    #time.sleep(0.5)
    
def check_website(address):
    """ 
Utility function: check if a website is down, if so, notify the user 
"""
    #try:
    val = ping_website(address)
    return val
    #except WebsiteDownException:
        #notify_owner(address)
    #    return 0







@celery.task(name="pings", time_limit=60)
def check_website_task(address):
    val = check_website(address)
    file = open('status.csv','a+')    
    file.write("\n")
    file.write(f"{address},{val}")
    file.close()
    return val
    




if __name__ == "__main__":
    app.run(debug=True)

