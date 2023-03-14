import requests
from app.load_configuration import get_urls
import json

def get_status_code():
  urls = get_urls()
  url_status_code = []

  for url in urls:
    r = requests.get(url, timeout=30.0)
    status_code = r.status_code
    url_status_code.append({'url': url, 'status': status_code})
  return url_status_code
  
def get_failure_tasks():
  CODIGOS_EXITOSOS = (200,201,206)
  url = "http://192.168.60.199:5555/api/tasks?state=FAILURE"
  print("Accediendo a : ", url)
  response = requests.get(url=url, timeout=30.0)
  status_code = response.status_code
  if status_code in CODIGOS_EXITOSOS:
      exceptions = []
      response_json = json.loads(response.text)
      #print (len(response_json), response_json['99ae2014-979e-430c-884d-1a493ad924c5']['exception'])
      i=0
      TimeLimitExceeded=0
      NoneType=0
      for task in response_json:
        i = i + 1
        if 'TimeLimitExceeded' in response_json[task]['exception']: 
          TimeLimitExceeded = TimeLimitExceeded + 1
        if 'object is not iterable' in response_json[task]['exception']: 
          NoneType = NoneType + 1
        #print(f" {i} : {response_json[task]['exception']} : {response_json[task]['uuid']}")
      
      print("TimeLimitExceeded, NoneType, Failure", TimeLimitExceeded, NoneType, len(response_json))
      exceptions.append({'flower_task_limit_exception': 'TimeLimitExceeded(60)', 'count': TimeLimitExceeded})
      exceptions.append({'flower_task_none_type_exception': 'TypeError(NoneType object is not iterable")', 'count': NoneType})
      exceptions.append({'flower_task_statuss': 'FAILURE', 'count': len(response_json)})
      exceptions.append({'url': 'www...ww', 'status': 201})

      return exceptions
