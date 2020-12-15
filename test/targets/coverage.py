import multiplication_or_sum
import unittest

class TestAdd(unittest.TestCase):
	def test_multiplication_or_sum(self):
		multiplication_or_sum.multiplication_or_sum(0, 0)
		multiplication_or_sum.multiplication_or_sum(-32, -32)
	


	
		

if __name__ == '__main__':
	unittest.main()