# -*- coding: utf-8 -*-

class AppError(Exception):
	status_code = 409

#	def __init__(self, errmsg, status_code=None, payload=None, debug=False):
# for dev only
	def __init__(self, errmsg, status_code=None, payload=None, debug=True):
		Exception.__init__(self)
		self.errmsg = errmsg
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload
		self.debug = debug

	def to_dict(self):
		if self.debug:
			rv = dict( self.payload or () )
		else:
			rv = dict( () )
		rv['errmsg'] = self.errmsg
		return rv


if __name__ == '__main__':
	error = AppError("test app error", 400)
	raise error

# vim:noet:ts=4:sw=4
