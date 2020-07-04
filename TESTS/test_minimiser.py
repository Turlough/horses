import unittest
import minimiser

from minimiser import Minimiser

m = Minimiser()


class TestMinimiser(unittest.TestCase):

    def test_submit_for_result(self):
        m.submit(5, "five")
        self.assertEqual('five', m.result())
        m.submit(4, "four")
        self.assertEqual('four', m.result())
        m.submit(6, "six")
        self.assertEqual('four', m.result())
        m.submit(2.1, "decimal")
        self.assertEqual('decimal', m.result())


if __name__ == '__main__':
    unittest.main()
