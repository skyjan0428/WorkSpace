
import unittest
import string_find
import string_in
import string_iter
import string_others
import string_replace
import string_slice
import string_startswith

class TestAdd(unittest.TestCase):
	def test_string_find(self):
		string_find.string_find('ggg', '')
		string_find.string_find('aaaaa2ggg', '')
	def test_string_in(self):
		string_in.string_in('abc', '')
		string_in.string_in('', '')

	def test_string_slice(self):
		string_slice.string_slice('', '')

	def test_string_iter(self):
		string_iter.string_iter('a', '')

	def test_string_others(self):
		pass

	def test_string_replace(self):
		string_replace.string_replace('AAAAEABAC@DAADAAAL#AGAAAAAAKAAA!AJa24AAABAA3dCAAAAAA63AAEAAR51AAMAAAA2AFAAAADAHAAAAABCAAAAA', '')
		string_replace.string_replace('', 'a eb3c hak')
		string_replace.string_replace('', '')

	def test_string_startswith(self):
		string_startswith.string_startswith('abcdefk1e', '')
		string_startswith.string_startswith('','')










	
		

if __name__ == '__main__':
	unittest.main()