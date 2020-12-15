import add_binary
import unittest
import addStrings
import restoreIpAddresses
import validIPAddress
import validWordAbbreviation

class TestAdd(unittest.TestCase):
	def test_add_binary(self):
		add_binary.add_binary('','')
		add_binary.add_binary("1", "1")

	def test_addStrings(self):
		addStrings.addStrings('','')
		addStrings.addStrings('99','9')
		addStrings.addStrings('90999','99')
		addStrings.addStrings('9','99999')
		addStrings.addStrings('1','11')

	def test_restoreIpAddresses(self):
		restoreIpAddresses.restoreIpAddresses('1023')
		restoreIpAddresses.restoreIpAddresses('1324')
		restoreIpAddresses.restoreIpAddresses('1926')
		restoreIpAddresses.restoreIpAddresses('/')
		restoreIpAddresses.restoreIpAddresses('1230')
		restoreIpAddresses.restoreIpAddresses('120')
		restoreIpAddresses.restoreIpAddresses('11012')

	def test_validIPAddress(self):
		pass


	def test_validWordAbbreviation(self):
		validWordAbbreviation.validWordAbbreviation("", "0")
		validWordAbbreviation.validWordAbbreviation("", "")
		validWordAbbreviation.validWordAbbreviation("0", "")
		validWordAbbreviation.validWordAbbreviation("", "1/")
		validWordAbbreviation.validWordAbbreviation("00", "1/")






	
		

if __name__ == '__main__':
	unittest.main()