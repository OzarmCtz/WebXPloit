# cython: language_level=3


import unittest

from src.utils.specifics.specific import format_url


class TestFormatURL(unittest.TestCase):
    def test_with_http(self):
        self.assertEqual(format_url("http://1.1.1.1:80"), "http://1.1.1.1")

    def test_with_https(self):
        self.assertEqual(format_url("https://1.1.1.1:443"), "https://1.1.1.1")

    def test_with_port_8080(self):
        self.assertEqual(format_url("1.1.1.1:8080"), "http://1.1.1.1:8080")

    def test_with_port_8443(self):
        self.assertEqual(format_url("1.1.1.1:8443"), "http://1.1.1.1:8443")

    def test_with_no_protocol_and_no_port(self):
        self.assertEqual(format_url("1.1.1.1"), "http://1.1.1.1")

    def test_with_unusual_port(self):
        self.assertEqual(format_url("1.1.1.1:1234"), "http://1.1.1.1:1234")

    def test_with_https_and_unusual_port(self):
        self.assertEqual(format_url("https://1.1.1.1:1234"), "https://1.1.1.1:1234")


if __name__ == "__main__":
    unittest.main()
