import unittest

#import sys
#sys.path.insert(0,'..')
from misc import *

class TestMisc(unittest.TestCase):

    def test_epoch_to_date_short(self):
        epoch = 1522705836
        date_str = convert_epoch_to_date(epoch)
        assert date_str == 'Apr 02'

    def test_epoch_to_date_long(self):
        epoch = 1522705836
        date_str = convert_epoch_to_date(epoch, False)
        assert date_str == 'Mon, 02 Apr 2018 17:50:36 EDT'

if __name__ == '__main__':
    unittest.main()
