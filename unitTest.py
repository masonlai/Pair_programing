import unittest
from unittest.mock import patch
from pair import tax_calculator
import io
import sys


class TestStringMethods(unittest.TestCase):
    @patch('builtins.input', side_effect=['y', '10000'])
    def test_single(self, m):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        tax_calculator()
        sys.stdout = sys.__stdout__
        result = """---------------------  -------
                    BASIC ALLOWANCES        132000
                    MPF ALLOWANCES             500
                    NET CHARGEABLE INCOME  -122500
                    TAX PAYABLE                  0
                    ---------------------  -------"""
        self.assertTrue(result, capturedOutput.getvalue())

    @patch('builtins.input', side_effect=['n', '100000', '100000'])
    def test_joint(self, m):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        tax_calculator()
        sys.stdout = sys.__stdout__
        result = """                            Self    Spouse
                    --------------------------  ------  --------
                    BASIC ALLOWANCES            132000  132000
                    MPF ALLOWANCES              5000    5000
                    NET CHARGEABLE INCOME       -37000  -37000
                    TAX PAYABLE (* Stand Rate)  0       0
                    Under Separate Taxation:    0
                    
                    -------------------------------------  ------
                    Joint BASIC ALLOWANCES                 264000
                    Joint MPF ALLOWANCES                    10000
                    Joint NET CHARGEABLE INCOME            -74000
                    Under Joint Assessment (* Stand Rate)       0
                    -------------------------------------  ------
                    Recommendation: You don't have to pay
                    """
        self.assertTrue(result, capturedOutput.getvalue())


if __name__ == '__main__':
    unittest.main()
