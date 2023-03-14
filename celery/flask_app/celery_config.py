from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    #celery = Celery('simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
    # celery.conf.update(app.config)
    # celery.conf.enable_utc = False
    # celery.conf.update(timezone = 'America/Mexico_City')

    #Celery beat settings
    # app.conf.beat_schedule = {
    #     'update_one_sucursal_every_3_min':{
    #         'task': 'update_sucursal',
    #         'schedule': crontab(minute='*/15')
    #     }
    # }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery