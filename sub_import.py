
# Imported by call_obj.py

import sub_sub_import

class TheSubClass:
    def __init__(self, value):
        self.sub = sub_sub_import.TheSubSubClass(value)
        self.value = sub_sub_import.sub_sub_func(value, value)
        self.value = value

    def __str__(self):
        return self.value

def sub_func(a, b):
    if a > b:
    	return b
    return a
