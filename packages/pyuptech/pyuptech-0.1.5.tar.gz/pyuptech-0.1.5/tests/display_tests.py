import unittest

from pyuptech import (
    set_emulation_mode,
    adc_io_display_on_console,
    mpu_display_on_console,
)


class DisplayTests(unittest.TestCase):

    def setUp(self):
        set_emulation_mode("off")

    def test_something(self):
        adc_io_display_on_console()
        mpu_display_on_console()


if __name__ == "__main__":
    unittest.main()
