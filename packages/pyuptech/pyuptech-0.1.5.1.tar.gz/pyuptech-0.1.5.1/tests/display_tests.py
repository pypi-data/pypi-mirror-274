import unittest

from pyuptech import (
    make_adc_io_table,
    make_mpu_table,
)
from pyuptech.modules.screen import Screen
from pyuptech.modules.sensors import OnBoardSensors


class DisplayTests(unittest.TestCase):

    def setUp(self):
        self.sen = OnBoardSensors()
        self.scr = Screen()

    def test_something(self):
        make_adc_io_table(self.sen)
        make_mpu_table(self.sen)


if __name__ == "__main__":
    unittest.main()
