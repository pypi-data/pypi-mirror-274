import unittest
from time import sleep

from pyuptech import make_mpu_table, make_adc_table, make_io_table
from pyuptech.modules.screen import Screen, Color
from pyuptech.modules.sensors import OnBoardSensors


class DisplayTests(unittest.TestCase):

    def setUp(self):
        self.sen = OnBoardSensors().adc_io_open().MPU6500_Open().set_all_io_mode(1)
        self.scr = Screen()

    def test_something(self):
        print(make_mpu_table(self.sen))
        print(make_io_table(self.sen))
        print(make_adc_table(self.sen))

    def test_led(self):
        for c in Color:
            self.scr.set_led_color(0, c)
            print(f"\rnow is {c}", end="")
            sleep(1)


if __name__ == "__main__":
    unittest.main()
