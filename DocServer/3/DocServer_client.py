import xmlrpc.client
sp = xmlrpc.client.ServerProxy('http://127.0.0.1:8002')

# register_instance

generated1 = sp.generate_html('*title')
generated2 = sp.generate_html('*content')
generated = generated1 + generated2

if 'script' in generated:
	return 'Error'
# register_function()
# sp.generate_html_func()