"""base.py のテスト"""

import unittest
from datetime import date
from dpc import LineBase


class TestLineBase(unittest.TestCase):
    """LineBaseクラスのテスト"""

    def test_to_float(self):
        """to_floatメソッドのテスト"""
        self.assertEqual(LineBase.to_float('123.45'), 123.45)
        self.assertIsNone(LineBase.to_float(''))

    def test_to_int(self):
        """to_intメソッドのテスト"""
        self.assertEqual(LineBase.to_int('123'), 123)
        self.assertEqual(LineBase.to_int('123.45'), 123)
        self.assertIsNone(LineBase.to_int(''))

    def test_to_bool(self):
        """to_boolメソッドのテスト"""
        self.assertTrue(LineBase.to_bool('1'))
        self.assertFalse(LineBase.to_bool('0'))
        self.assertIsNone(LineBase.to_bool(''))

    def test_to_date(self):
        """to_dateメソッドのテスト"""
        self.assertEqual(LineBase.to_date('20210520'), date(2021, 5, 20))
        self.assertIsNone(LineBase.to_date('00000000'))
        self.assertIsNone(LineBase.to_date(''))

    def test_yyyymmdd(self):
        """yyyymmddメソッドのテスト"""
        self.assertEqual(LineBase.yyyymmdd(date(2021, 5, 20)), '20210520')
        self.assertEqual(LineBase.yyyymmdd(None), '00000000')


if __name__ == '__main__':
    unittest.main()
