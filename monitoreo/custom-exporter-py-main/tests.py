from app.app import  get_status_code
from app.app import  get_failure_tasks


for status in get_status_code():
  print(status)


print("failure: ",get_failure_tasks())
