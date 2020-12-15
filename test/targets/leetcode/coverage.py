import add_digits
import unittest
import fraction_to_decimal
import reverseCheck
import ugly_number

class TestAdd(unittest.TestCase):
	def test_add_digits(self):
		add_digits.add_digits(0)
		add_digits.add_digits(12)
		add_digits.add_digits(9)
	def test_fraction_to_decimal(self):
		fraction_to_decimal.fraction_to_decimal(0,0)
		fraction_to_decimal.fraction_to_decimal(2,0)
		fraction_to_decimal.fraction_to_decimal(2,2)
		fraction_to_decimal.fraction_to_decimal(-16,8)

	def test_reverseCheck(self):
		reverseCheck.reverseCheck(0)
		reverseCheck.reverseCheck(2)
		reverseCheck.reverseCheck(-16)
		reverseCheck.reverseCheck(12)
		reverseCheck.reverseCheck(11)

	def test_ugly_number(self):
		ugly_number.ugly_number(0)
		ugly_number.ugly_number(2)
		ugly_number.ugly_number(3)
		ugly_number.ugly_number(1)
		ugly_number.ugly_number(5)
	


	
		

if __name__ == '__main__':
	unittest.main()