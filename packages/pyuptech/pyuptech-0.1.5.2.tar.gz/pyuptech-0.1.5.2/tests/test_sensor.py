import unittest
from unittest import skip

from pyuptech import OnBoardSensors


class DisplayTests(unittest.TestCase):

    def setUp(self):
        self.sen = OnBoardSensors().MPU6500_Open().adc_io_open()

    def test_adc(self):
        print(self.sen.adc_all_channels())

    def test_io(self):
        print(self.sen.set_all_io_mode(0).set_all_io_level(1).io_all_channels())

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
