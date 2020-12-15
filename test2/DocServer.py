from xmlrpc.server import DocXMLRPCServer

# register_instance的做法

class doc_generate:
	def __init__(self, serv):
		self.serv = serv

	def generate_html(self, title):
		import traceback
		traceback.print_stack()
		self.serv.set_server_title(title)
		generated = self.serv.generate_html_documentation()
		if 'script' in generated:
		    return 'Error'
		return generated

def main():
    serv = DocXMLRPCServer(("localhost", 8002), logRequests=False)
    # print(serv.RequestHandlerClass)
    # exit()
    serv.register_instance(doc_generate(serv))
    # generate_html_func() 
    serv.serve_forever()

# main()


# serv = DocXMLRPCServer(("localhost", 8000), logRequests=False)
# serv.register_instance(doc_generate(serv))
# # generate_html_func()
# serv.serve_forever()



