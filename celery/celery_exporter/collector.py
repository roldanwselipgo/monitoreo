import time
import os
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from app.app import  get_status_code, get_failure_tasks

class CustomCollector(object):
    def __init__(self):
      pass

    def collect(self):
      g = GaugeMetricFamily("flower_task_execptions", "This collector verify the status code of request", labels=['type'])
      
      #for row in get_status_code():
      #  g.add_metric([row['url']], row['status']) 
      
      print(get_failure_tasks())
      failure_tasks = get_failure_tasks()
      g.add_metric([failure_tasks[0]['flower_task_limit_exception']], failure_tasks[0]['count']) 
      g.add_metric([failure_tasks[1]['flower_task_none_type_exception']], failure_tasks[1]['count']) 
      g.add_metric([failure_tasks[2]['flower_task_statuss']], failure_tasks[2]['count']) 
      yield g
     
if __name__ == '__main__':
    start_http_server(5530)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)
