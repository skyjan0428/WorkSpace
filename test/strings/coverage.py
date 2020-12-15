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
		build_in.build_in(0, 0)
		build_in.build_in(112, 0)
		build_in.build_in(0, 2)
		build_in.build_in(95, 0)
		build_in.build_in(112, 2)
		build_in.build_in(100, -54)
		build_in.build_in(42, 53)
	def test_call_obj(self):
		call_obj.call_obj(0, 0)
		call_obj.call_obj(2, 0)

	def test_do_abs(self):
		do_abs.do_abs(0, 0)

	def test_do_array(self):
		do_array.do_array(0, 0)


	def test_do_numbers(self):
		do_numbers.do_numbers(0, 0)
		do_numbers.do_numbers(2, 0)
		do_numbers.do_numbers(-14, 0)
		do_numbers.do_numbers(114, 0)

	def test_do_range(self):
		do_range.do_range(0, 0)
		do_range.do_range(2, 0)

	def test_list_dict(self):
		list_dict.list_dict(0, 0)
		list_dict.list_dict(2, 0)

	def test_loop(self):
		loop.loop(0, 0)
		loop.loop(2, 0)
		loop.loop(0, 2)

	def test_while_loop(self):
		while_loop.while_loop(0, 0)










	
		

if __name__ == '__main__':
	unittest.main()