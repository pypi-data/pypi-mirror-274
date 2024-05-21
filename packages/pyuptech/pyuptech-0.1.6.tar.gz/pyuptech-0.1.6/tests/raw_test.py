from pyuptech import Color, Screen, OnBoardSensors

OnBoardSensors().adc_io_open()
scr = Screen(2)


for c in Color:
    scr.set_led_color(0, c)
    print(f"\rnow is {c},value:{c.value}", end="")
    input()
