from celery import Celery

__author__ = 'eduardo'

app = Celery('tasks', backend='amqp', broker='amqp://')

@app.task
def add(x, y):
    return x + y