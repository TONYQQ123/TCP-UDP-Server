import unittest
import time
import ast
import re
from Server.CServer import check_eq,Caculate

class TestEquationCalculator(unittest.TestCase):
    def test_check_eq_valid(self):
        self.assertTrue(check_eq("3 + 4"))
        self.assertTrue(check_eq("5 * 6 - 2"))
        self.assertTrue(check_eq("10 / 2 + 3"))
        self.assertTrue(check_eq("1+(3*4)/2"))
    
    def test_check_eq_invalid(self):
        self.assertFalse(check_eq("3a + +4b"))
        self.assertFalse(check_eq("5 * 6 - 2-!"))
        self.assertFalse(check_eq("10 / 2 +"))
    
    def test_Calculate_valid(self):
        self.assertEqual(Caculate("3 + 4"), {'success': 7, 'status': True})
        self.assertEqual(Caculate("5 * 6 - 2"), {'success': 28, 'status': True})
        self.assertEqual(Caculate("10 / 2 + 3"), {'success': 8, 'status': True})
        self.assertEqual(Caculate("8 * 2 / 4"), {'success': 4.0, 'status': True})
    
    def test_Calculate_invalid(self):
        result = Caculate("3a + 4b")
        self.assertFalse(result['status'])
        result = Caculate("5 * 6 - 2x")
        self.assertFalse(result['status'])
        result = Caculate("10 / 2 +")
        self.assertFalse(result['status'])
        result = Caculate("8 * 2 / 0")
        self.assertFalse(result['status'])

if __name__ == '__main__':
    unittest.main()
