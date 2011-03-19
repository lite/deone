import sys,random
from client import App3Client
import simplejson

c = App3Client('de-one.appspot.com', 'test', 'test')
#c = App3Client('localhost:8080', 'test', 'test')
#c = App3Client('localhost:8080', 'test', 'wrong_password')

#Deone
s = c.list('Deone')
print(s)
if s is not None:
    items = simplejson.loads(s)
    for item in items:
        id = item['id']
        print(id)
        #print(c.get('Deone', id))
        c.delete('Deone', id)
    #c.post('Deone', {"data": "1234567890123"})
