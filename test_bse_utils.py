

import tickerplot.bse.bse_utils as test_bse_utils

import unittest
from mock import Mock

class testBSEUtils(unittest.TestCase):

    def setUp(self):
        test_bse_utils.module_logger = Mock()


    def test_get_bse_all_stocks_list_invalid_start(self):

        test_start = 'foo'
        test_count = -1

        bse_utils_gen = test_bse_utils.bse_get_all_stocks_list(test_start, test_count)
        with self.assertRaises(ValueError) as context:
            next(bse_utils_gen)

        self.assertTrue(context)

    def test_get_bse_all_stocks_list_invalid_count(self):

        test_start = 0
        test_count = None

        bse_utils_gen = test_bse_utils.bse_get_all_stocks_list(test_start, test_count)
        with self.assertRaises(Exception) as context:
            next(bse_utils_gen)

        self.assertIsInstance(context.exception, TypeError)

    def test_requests_returns_not_ok(self):

        req = test_bse_utils.requests = Mock()

        mock_not_ok = Mock()
        mock_not_ok.ok = False
        req.get = Mock(return_value=mock_not_ok)

        bse_utils_gen = test_bse_utils.bse_get_all_stocks_list(start=0, count=-1)
        with self.assertRaises(StopIteration) as context:
            next(bse_utils_gen)

        self.assertTrue(context)

if __name__ == '__main__':
    unittest.main()
