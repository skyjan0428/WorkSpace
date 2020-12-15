import test
import unittest

class TestAdd(unittest.TestCase):
	def test_do_array(self):
		test.do_array(0, 0)

	def test_do_range(self):
		test.do_range(0, 0)

	def test_while_loop(self):
		test.while_loop(0,0)

	def test_do_numbers(self):
		test.do_numbers(-1, 0)
		test.do_numbers(1, 2)
		test.do_numbers(99, 100)
		test.do_numbers(101, 99)

	def test_loop(self):
		test.loop(2, 3)
		test.loop(1, 3)

	def test_do_abs(self):
		test.do_abs(5, 4)
		test.do_abs(3, 4)

	def test_add_digits(self):
		test.add_digits(10)
		test.add_digits(9)
		test.add_digits(1)

	def test_multiplication_or_sum(self):
		test.multiplication_or_sum(1, 2)
		test.multiplication_or_sum(3, 400)

	def test_string_in(self):
		test.string_in('abc', '')
		test.string_in('', '')

	def test_string_slice(self):
		test.string_slice('aaaaa', '')

	def test_string_iter(self):
		test.string_iter('a', '')
		

if __name__ == '__main__':
	unittest.main()