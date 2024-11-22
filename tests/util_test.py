import unittest

import src.util as util


class UtilTests(unittest.TestCase):
    def test_create_all_translations(self):
        # create
        abc_bca_cab = util.create_all_translations(("a", "b", "c"))

        # check
        self.assertCountEqual(
            abc_bca_cab, [("a", "b", "c"), ("b", "c", "a"), ("c", "a", "b")]
        )

if __name__ == '__main__':
    unittest.main()