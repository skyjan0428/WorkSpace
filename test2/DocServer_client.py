import xmlrpc.client
sp = xmlrpc.client.ServerProxy('http://127.0.0.1:8002')

# register_instance
def main():
	generated = sp.welcome_html('*title')
	if 'script' in generated:
		return 'Error'
	


# register_function()
# sp.generate_html_func()