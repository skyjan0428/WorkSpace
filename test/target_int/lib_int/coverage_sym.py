import datetime__parse_hh_mm_ss_ff
import unittest
import datetime__parse_isoformat_date
import http_parse_request
import ipaddress__ip_int_from_string
import distutils_get_build_version
import email__parsedate_tz
import wsgiref_check_status
import nntplib__parse_datetime
import smtpd_parseargs

class TestAdd(unittest.TestCase):
	def test_http_parse_request(self):
		http_parse_request.http_parse_request('')

	def test_ipaddress__ip_int_from_string(self):
		ipaddress__ip_int_from_string.ipaddress__ip_int_from_string('')

	def test_distutils_get_build_version(self):
		distutils_get_build_version.distutils_get_build_version('')
	
	def test_email__parsedate_tz(self):
		email__parsedate_tz.email__parsedate_tz('')

	def test_wsgiref_check_status(self):
		wsgiref_check_status.wsgiref_check_status('')

	def test_nntplib__parse_datetime(self):
		nntplib__parse_datetime.nntplib__parse_datetime('00120012120012')
		nntplib__parse_datetime.nntplib__parse_datetime('00780078780078')
		nntplib__parse_datetime.nntplib__parse_datetime('10000101111111')

	def test_datetime__parse_hh_mm_ss_ff(self):
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:00:00.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('000000000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:00:00.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('11:00:00.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('11:11:01.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('13:00:00.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('-1:00:00.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:61:00.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:-1:00.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:00:61.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:01:-1.000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:01:00:000000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:00:00.00000')
		datetime__parse_hh_mm_ss_ff.datetime__parse_hh_mm_ss_ff('00:00:00.000')

	def test_datetime__parse_isoformat_date(self):
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('')
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('1234-00000')
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('3456-00012')
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('0123-00000')
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('-123-00000')
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('0000000000')
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('0000-11000')
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('0000-11-01')
		datetime__parse_isoformat_date.datetime__parse_isoformat_date('0000-01-00')

	def test_smtpd_parseargs(self):
		smtpd_parseargs.smtpd_parseargs('', '')
		smtpd_parseargs.smtpd_parseargs('', '0')
		smtpd_parseargs.smtpd_parseargs('0', '')
		smtpd_parseargs.smtpd_parseargs('0:0', '')
		smtpd_parseargs.smtpd_parseargs('0:a', '')
		smtpd_parseargs.smtpd_parseargs('0:a', '0:0')

	

if __name__ == '__main__':
	unittest.main()