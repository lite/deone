#/usr/bin/env python2.5

"""
Cookie signed with a secret server's key.

While cookies are a convenient way to store data in clients' browsers,
they can be susceptible to forgery.  By attaching a signature to each
(key=value) pair, we can verify that the values the cookies carry are
really those issued by the server.

This implementation ensure that in a key=value cookie, the value is
really intended for the particular key.

Each cookie is signed with HMAC-SHA256.

SignedCookie inherits from SimpleCookie and share the same API.
A SignedCookie is constructed with a secret key as the argument.

>>> c = SignedCookie('Open, sesame!')
>>> c['user'] = 'username'
>>> c['user'].value
'username'
>>> c['user'].coded_value
'"usernameCu/vp7hQJ8QsnLoMvFyM6jwyqAyZMIdJcpUZRBE6JYU="'

Loading also works.

>>> c.load('Cookie: itemid="12345mwKEC0M1343j/uvi3DIwLsiQWw7UP0Ue/84NxBUwljI="; Max-Age=100')
>>> c['itemid'].value
'12345'
>>> int(c['itemid']['max-age'])
100
"""

import re
import hmac
from hashlib import sha256
from base64 import b64encode, b64decode
import Cookie


SIG_LEN = 44		# the length of a sha256 hash string is 32,
				# thus a base64 encoding of that block 
				# will always be of length 44

SIG_PATTERN = re.compile(r'[0-9a-zA-Z+/=]{44}')
# This is the regex pattern for the signature generated by SignedCookie
# which is base64 blob of length 44.

class BadSignatureError(Exception):
	pass

class SignedCookie(Cookie.SimpleCookie):
	def __init__(self, key, input=None):
		"""
		Initialize the Cookie with a secret key.
		"""
		self.key = key.encode('ascii')
		if input:
			self.load(input)
	
	def __setitem__(self, key, value):
		strval = str(value)
		sig = b64encode(
			hmac.new(self.key + str(key), strval, sha256).digest()
			)
		cval = Cookie._quote( strval + sig )
		self._BaseCookie__set(key, strval, cval)
	
	## Copied verbatim from Cookie.py
	## This has to be here to be able to use our implementation of __ParseString
	def load(self, rawdata):
		"""Load cookies from a string (presumably HTTP_COOKIE) or
		from a dictionary.  Loading cookies from a dictionary 'd'
		is equivalent to calling:
			map(Cookie.__setitem__, d.keys(), d.values())
		"""
		if type(rawdata) == type(""):
			self.__ParseString(rawdata)
		else:
			self.update(rawdata)
		return
	
	## Copied from Cookie.py
	## Changed the last block to use decode & verify signature
	def __ParseString(self, str, patt=Cookie._CookiePattern):
		i = 0			# Our starting point
		n = len(str)		# Length of string
		M = None		# current morsel

		while 0 <= i < n:
			# Start looking for a cookie
			match = patt.search(str, i)
			if not match: break		  # No more cookies

			K,V = match.group("key"), match.group("val")
			i = match.end(0)

			# Parse the key, value in case it's metainfo
			if K[0] == "$":
				# We ignore attributes which pertain to the cookie
				# mechanism as a whole.  See RFC 2109.
				# (Does anyone care?)
				if M:
					M[ K[1:] ] = V
			elif K.lower() in Cookie.Morsel._reserved:
				if M:
					M[ K ] = Cookie._unquote(V)
			else:
				if not SIG_PATTERN.search(V):
					pass
				uval = Cookie._unquote(V)
				real_val = uval[:-SIG_LEN]
				try:
					sig = b64decode( uval[-SIG_LEN:] )
				except TypeError:
					# Incorrect padding
					raise BadSignatureError("Bad signature for cookie '%s'" % K)
				# TODO: use constant time string comparison
				if sig != hmac.new(self.key + K, real_val, sha256).digest():
					raise BadSignatureError("Bad signature for cookie '%s'" % K)
				self._BaseCookie__set(K, real_val, V)
				M = self[K]
