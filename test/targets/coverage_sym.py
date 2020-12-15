import multiplication_or_sum
import unittest
import count_emma
import regex

class TestAdd(unittest.TestCase):
	def test_multiplication_or_sum(self):
		multiplication_or_sum.multiplication_or_sum(1, 2)
		multiplication_or_sum.multiplication_or_sum(3, 400)

	def test_count_emma(self):
		pass

	def test_regex(self):
		regex.regex('12')
		regex.regex('')

	


	
		

if __name__ == '__main__':
	unittest.main()