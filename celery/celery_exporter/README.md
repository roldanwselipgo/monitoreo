# custom-exporter-py

This project is used to complement the tutorial published on the following page: https://blog-ocampoge.medium.com/prometheus-exporters-personalizados-con-python-61f87d8530ad

## Usage
> This collector verify the status code of request

Specify the urls you want to get the response status code

```
---
urls:
  - 'https://www.google.com.py'
  - 'http://medium.com'
  - 'https://www.python.org/'
```

Install dependencies

```
pip install -r requirements.txt
```

Run the collector

```
python collector.py
```

Verify the browsera in the port 5530

```
http://localhost:5530/
```
