# -*- coding: utf-8 -*-

import httplib2
#import urllib2
#import httplib
from auth import generate_auth, generate_timestamp
import random, time
import simplejson

class App3Client(object):
    """
    Simple REST Client for App3.
    """
    def __init__(self, host, user_name='test', user_pass='test'):
        self.__host = host
        self.__user_name = user_name
        self.__user_pass = user_pass
        self.h = httplib2.Http()
        
    def post(self, resource, params=None):
        """
        Executes a POST request on the specified resource.
        """
        resp, body = self.__request(
            method = 'POST', 
            url = "/rest/%s/" % (resource), 
            params = params,
        )
        #print(resp, body)
        if (resp is not None) and (resp['status'] == '201'): 
            return body
        else: 
            return None

    def list(self, resource, params=None):
        """
        Lists the all of the resources of type resource.
        """
        resp, body = self.__request(
            method = 'GET', 
            url = "/rest/%s/" % resource, 
            params = params,
        )

        if (resp is not None) and (resp['status'] == '200'): 
            return body
        else: 
            return None
    
    def get(self, resource, id, params=None):
        """
        Retrieves the resource specified.
        """
        resp, body = self.__request(
            method = 'GET', 
            url = "/rest/%s/%s/" % (resource, id), 
            params = params,
        )
        
        if (resp is not None) and (resp['status'] == '200'): 
            return body
        else: 
            return None
    
    def exists(self, resource, id):
        """
        Returns whether the resource specified exists in the datastore.
        """
        resp = self.__request(
            method = 'GET', 
            url = "/rest/%s/%s/" % (resource, id), 
        )
        return (resp is not None) and (resp['status'] == '200')
        
    def delete(self, resource, id):
        """
        Deletes the specified resource from the datastore.
        """
        resp, body = self.__request(
            method = 'DELETE', 
            url = "/rest/%s/%s/" % (resource, id), 
        )
        #print(resp, body)
        if (resp is not None) and (resp['status'] == '200'): 
            return body
        else: 
            return None
    
    def test(self):
        resp, body = self.__request(
            method = 'GET', 
            url = "/",
        )
        
        if (resp is not None) and (resp['status'] == '200'): 
            return body
        else: 
            return None
    
    def __request(self, method, url, params=None):
        """
        Internal method for executing all of the REST requests.
        """
        if params is not None:
            params = simplejson.dumps(params)
                
        self.app3_timestamp = generate_timestamp()

        headers = {
            #"Content-type": "application/json",
            'App3-User': self.__user_name,
            'App3-Pass': self.__user_pass,
            'App3-Timestamp': self.app3_timestamp,
            'App3-Auth': generate_auth(self.__user_name, self.app3_timestamp),
        }
        
        #h = httplib2.Http(".cache")
        #h.add_credentials('name', 'password')
        resp, body = self.h.request("http://"+self.__host + url, method, body=params, headers=headers )
        #print(resp, body)
        return resp, body

#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    from client import App3Client
    c = App3Client('de-one.appspot.com', 'test', 'test')
    print(c.test())
    print(c.list('Deone'))
        