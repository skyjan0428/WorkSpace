from xmlrpc.server import DocXMLRPCServer


# register_instance的做法

class doc_generate:
	def __init__(self, serv):
		self.serv = serv
	
	def welcome_html(self, title):

		generated = '<html><head><title>' + title + '</title></head><body>Welcome</body></html>'
		return generated
	def generate_html(self, title):

		self.serv.set_server_title(title)
		generated = self.serv.generate_html_documentation()
		return generated

def main():
	# import builtins
	# from types import FunctionType
	# func = FunctionType(doc_generate, {}, argdefs= ())
	# a = builtins.__build_class__(fnc, 'doc_generate')
	# print(type(doc_generate))
	serv = DocXMLRPCServer(("localhost", 8002), logRequests=False)
	serv.register_instance(doc_generate(serv))
	serv.serve_forever()

# main()


# serv = DocXMLRPCServer(("localhost", 8000), logRequests=False)
# serv.register_instance(doc_generate(serv))
# # generate_html_func()
# serv.serve_forever()



