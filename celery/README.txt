

[EJECUCION]
cd /usr/local/VRec4/celery
docker-compose build && docker-compose up


[OTROS COMANDOS]
redis-server
flask --app app run --host=0.0.0.0
celery -A app.celery worker --loglevel=info --concurrency=10
celery -A app.celery worker -P eventlet -c 600
celery -A app.celery flower  --address=0.0.0.0 --port=5566
celery -A app.celery beat --loglevel=info
celery -A <myproject> control enable_events

[INSTALACIONES Y CONFIGURACIONES EXTRA]

/usr/local/VRec4/celery/docker-compose.yml
  - job_name: 'docker'
    static_configs:
    - targets: ['{$IP_MACHINE}:9323'] 