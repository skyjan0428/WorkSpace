import build_in
import unittest
import call_obj
import do_abs
import do_array
import do_numbers
import do_range
import list_dict
import loop
import while_loop

class TestAdd(unittest.TestCase):
	def test_build_in(self):
		pass
	def test_call_obj(self):
		call_obj.call_obj(0, 0)

	def test_do_abs(self):
		do_abs.do_abs(5, 4)
		do_abs.do_abs(3, 4)

	def test_do_array(self):
		do_array.do_array(0, 0)


	def test_do_numbers(self):
		do_numbers.do_numbers(-1, 0)
		do_numbers.do_numbers(1, 2)
		do_numbers.do_numbers(99, 100)
		do_numbers.do_numbers(101, 99)

	def test_do_range(self):
		do_range.do_range(0, 0)

	def test_list_dict(self):
		list_dict.list_dict(0, 0)
		list_dict.list_dict(2, 0)

	def test_loop(self):
		loop.loop(2, 3)
		loop.loop(1, 3)
		
	def test_while_loop(self):
		while_loop.while_loop(0, 0)










	
		

if __name__ == '__main__':
	unittest.main()