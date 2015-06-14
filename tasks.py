from celery import Celery
from ProbeModules.SSLConnection import SSLConnection

__author__ = 'eduardo'

app = Celery('tasks', backend='amqp', broker='amqp://')

@app.task
def certificate(ip):
    ssl_connection = SSLConnection(ip, 443, False)
    cert = ssl_connection.get_formatted_certificate().data_dict()
    ssl_connection.close()
    return cert