from celery import group

from tasks import certificate

__author__ = 'eduardo'

if __name__ == '__main__':
    ip_list = [('152.74.95.1',), ('152.74.75.106',), ('164.77.245.172',), ('164.77.211.2',), ('146.155.200.30',)]
          #('152.74.120.225',), ('186.67.196.26',), ('164.77.220.219',), ('186.67.134.58',), ('164.77.129.146',),
          #('164.77.171.211',), ('186.67.171.218',), ('186.67.145.228',), ('186.67.163.107',), ('186.67.180.161',),
          #('164.77.177.163',), ('216.155.86.9',), ('164.77.153.9',), ('152.74.119.1',),  ('186.67.144.148',),
          #('186.67.168.36',), ('216.155.75.66',), ('186.67.148.229',), ('186.67.180.202',), ('164.77.228.202',),
          #('164.77.163.155',), ('164.77.204.135',), ('186.67.189.102',)]

    job = group(certificate.subtask(ip) for ip in ip_list)
    result = job.apply_async()
    print result.completed_count()
    print result.join()