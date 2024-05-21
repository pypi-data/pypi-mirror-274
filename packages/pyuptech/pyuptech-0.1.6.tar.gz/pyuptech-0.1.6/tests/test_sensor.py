import time
import unittest
from unittest import skip

from pyuptech import OnBoardSensors, set_log_level

set_log_level("DEBUG")


class DisplayTests(unittest.TestCase):

    def setUp(self):
        self.sen = OnBoardSensors().MPU6500_Open().adc_io_open()

    def test_adc(self):
        print(self.sen.adc_all_channels())

    def test_io(self):
        self.sen.set_all_io_mode(0)
        time.sleep(0.1)
        print(f"{self.sen.io_all_channels():08b}")
        self.sen.set_all_io_mode(0).set_all_io_levels(
            0
        )  # not support set at input mode
        time.sleep(0.1)
        print(f"ios:{self.sen.io_all_channels():08b}")

        print("test output mode set all bit")
        self.sen.set_all_io_mode(1)
        for i in [
            0b00000001,
            0b00000010,
            0b00000100,
            0b00001000,
            0b00010000,
            0b00100000,
            0b01000000,
            0b10000000,
        ]:
            self.sen.set_all_io_levels(i)
            time.sleep(0.1)
            print(f"{self.sen.io_all_channels():08b}")

        self.sen.set_all_io_mode(1)

        self.sen.set_io_mode(3, 0)
        self.sen.set_io_mode(0, 0)
        self.sen.set_io_mode(7, 0)
        time.sleep(1)

        print(f"modes:{self.sen.get_all_io_mode():08b}")
        print(f"ios:{self.sen.io_all_channels():08b}")

        print(f"set index 2 to output")
        self.sen.set_io_mode(2, 1)
        print(f"modes:{self.sen.get_all_io_mode():08b}")
        print(f"ios:{self.sen.io_all_channels():08b}")
        print(f"flip index 2")
        self.sen.flip_io_level(2)
        print(f"modes:{self.sen.get_all_io_mode():08b}")
        print(f"ios:{self.sen.io_all_channels():08b}")

    def test_mpu(self):
        print(self.sen.atti_all())
        print(self.sen.gyro_all())
        print(self.sen.acc_all())
        print("finished")

    @skip
    def test_mpu_freq(self):
        from utils import time_it

        print(time_it(self.sen.acc_all)())
        print(time_it(self.sen.atti_all)())
        print(time_it(self.sen.gyro_all)())

    def test_mpu_set_get(self):

        print(self.sen.get_acc_fsr())
        print(self.sen.get_gyro_fsr())
        g_fsr = 250
        self.sen.mpu_set_gyro_fsr(g_fsr)
        a_fsr = 2
        self.sen.mpu_set_accel_fsr(a_fsr)
        self.assertEqual(self.sen.get_acc_fsr(), a_fsr)
        self.assertEqual(self.sen.get_gyro_fsr(), g_fsr)


if __name__ == "__main__":
    unittest.main()
