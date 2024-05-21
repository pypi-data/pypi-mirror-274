import unittest

from pyuptech import make_mpu_table, make_adc_table, make_io_table
from pyuptech.modules.screen import Screen
from pyuptech.modules.sensors import OnBoardSensors


class DisplayTests(unittest.TestCase):

    def setUp(self):
        self.sen = OnBoardSensors().adc_io_open().MPU6500_Open()
        self.scr = Screen()

    def test_something(self):
        print(make_mpu_table(self.sen))
        print(make_io_table(self.sen))
        print(make_adc_table(self.sen))


if __name__ == "__main__":
    unittest.main()
