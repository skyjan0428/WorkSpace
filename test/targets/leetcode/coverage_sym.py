import add_digits
import unittest
import fraction_to_decimal
import reverseCheck
import ugly_number
import findUnsortedSubarray
import isLongPressedName
import numDecodings
import substring
import substring2

class TestAdd(unittest.TestCase):
	def test_add_digits(self):
		add_digits.add_digits(10)
		add_digits.add_digits(9)
		add_digits.add_digits(1)

	def test_findUnsortedSubarray(self):
		findUnsortedSubarray.findUnsortedSubarray('')
		findUnsortedSubarray.findUnsortedSubarray('4346')

	def test_isLongPressedNamey(self):
		isLongPressedName.isLongPressedName('ajcc', 'x1ajcc7o')
		isLongPressedName.isLongPressedName('a', '')
		isLongPressedName.isLongPressedName('wcca', 'wccc3oe')



	def test_numDecodings(self):
		numDecodings.numDecodings('423')
		numDecodings.numDecodings('226')
		numDecodings.numDecodings('')

	def test_fraction_to_decimal(self):
		fraction_to_decimal.fraction_to_decimal(0,0)
		fraction_to_decimal.fraction_to_decimal(2,0)
		fraction_to_decimal.fraction_to_decimal(2,2)
		fraction_to_decimal.fraction_to_decimal(-1,17)
		fraction_to_decimal.fraction_to_decimal(-10,3)

	def test_reverseCheck(self):
		reverseCheck.reverseCheck(10)
		reverseCheck.reverseCheck(0)


	def test_ugly_number(self):
		ugly_number.ugly_number(0)
		ugly_number.ugly_number(2)
		ugly_number.ugly_number(3)
		ugly_number.ugly_number(1)
		ugly_number.ugly_number(5)

	def test_substring(self):
		substring.substring('')
		substring.substring('jeiwa1j3')

	def test_substring2(self):
		substring2.substring2('')
		substring2.substring2('a3ja3wkc#od')
		substring2.substring2('f')
	


	
		

if __name__ == '__main__':
	unittest.main()