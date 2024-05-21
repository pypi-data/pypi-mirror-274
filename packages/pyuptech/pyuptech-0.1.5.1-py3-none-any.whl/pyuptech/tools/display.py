import time
from typing import Literal, Dict

from ..modules.screen import Screen, Color, FontSize
from ..modules.sensors import OnBoardSensors


def mpu_display_on_lcd(
    screen: Screen, sensors: OnBoardSensors, mode: Literal["atti", "acc", "gyro"]
):
    """
    Display the specified mode on the screen.

    Parameters:
        screen: An instance of the `Screen` class.
        sensors: An instance of the `OnBoardSensors` class.
        mode (Literal["atti", "acc", "gyro"]): The mode to display.

    Returns:
        None
    """
    match mode:
        case "atti":
            attitude = sensors.atti_all()
            screen.put_string(0, 30, f"Pitch:{attitude[0]:.2f}  ")
            screen.put_string(0, 48, f"Roll :{attitude[1]:.2f}  ")
            screen.put_string(0, 66, f"Yaw  :{attitude[2]:.2f}  ")
        case "gyro":
            gyro = sensors.gyro_all()
            screen.put_string(0, 30, f"Gyro X {gyro[0]:.2f}")
            screen.put_string(0, 48, f"Gyro Y {gyro[1]:.2f}")
            screen.put_string(0, 66, f"Gyro Z {gyro[2]:.2f}")
        case "acc":
            accel = sensors.acc_all()
            screen.put_string(0, 30, f"ACC X :{accel[0]:.2f}")
            screen.put_string(0, 44, f"ACC Y :{accel[1]:.2f}")
            screen.put_string(0, 54, f"ACC Z :{accel[2]:.2f}")
    screen.refresh()


def make_mpu_table(sensors: OnBoardSensors) -> str:
    """
    Generate and return a formatted string containing a table with accelerometer, gyroscope, and attitude information.

    This function extracts acceleration, gyroscope, and attitude data from sensor readings and formats it into an
    aesthetically pleasing table, displaying the values for each axis of acceleration, gyroscope, and attitude angles.

    Parameters:
        sensors: An instance of the `OnBoardSensors` class.

    Returns:
        str: A formatted table string.
    """
    from terminaltables import DoubleTable

    # Initialize the data list to store table data
    combined_data = [
        ["ACC", "Value", "GYRO", "Value", "ATTI", "Value"],
    ]
    acc_names = ["X_ACC", "Y_ACC", "Z_ACC"]

    gyro_names = ["X_GYRO", "Y_GYRO", "Z_GYRO"]

    atti_names = ["Pitch", "Roll", "Yaw"]
    # Iterate through acceleration, gyroscope, and attitude data, adding them to the combined_data list
    for i in range(len(acc_names)):
        combined_data.append(
            [
                acc_names[i],
                f"{sensors.acc_all()[i]:.2f}",  # Acceleration value
                gyro_names[i],
                f"{sensors.gyro_all()[i]:.2f}",  # Gyroscope value
                atti_names[i],
                f"{sensors.atti_all()[i]:.2f}",  # Attitude value
            ]
        )

    # Create a table using the DoubleTable class and customize its style
    table = DoubleTable(combined_data)
    table.inner_row_border = True  # Add inner row borders for improved readability
    return table.table


def make_adc_io_table(
    sensors: OnBoardSensors,
    adc_labels: Dict[int, str] = None,
    io_labels: Dict[int, str] = None,
) -> str:
    """
    Generate and return a formatted string table containing ADC (Analog-to-Digital Converter) and IO (Input/Output) channel information.

    Parameters:
        sensors: An instance of the `OnBoardSensors` class.
        adc_labels: A dictionary mapping ADC channel numbers (int) to custom names (str). Defaults to None, indicating no custom names are used.
        io_labels: A dictionary mapping IO channel numbers (int) to custom names (str). Defaults to None, indicating no custom names are used.

    Returns:
        A string representation of the table, formatted using the terminaltables library.

    Dependencies:
        This function relies on external functions `adc_all_channels()`, `io_all_channels()`, and `get_all_io_mode()` from the `sensors` module.
    """

    from terminaltables import (
        DoubleTable,
    )  # Import library for formatting the table output

    # Use empty dictionaries as default values if adc_labels or io_labels are not provided
    adc_labels = adc_labels or {}
    io_labels = io_labels or {}

    # Retrieve all ADC and IO channel data from the sensors module
    adc = sensors.adc_all_channels()
    io = sensors.io_all_channels()
    io_modes = sensors.get_all_io_mode()

    # Construct the rows of the table
    rows = [
        ["ADC Name"]
        + [adc_labels.get(i, f"ADC{i}") for i in range(10)],  # ADC Name row
        ["ADC Data"] + [f"{x}" for x in adc],  # ADC Data row
        ["IO Name"] + [io_labels.get(i, f"IO{i}") for i in range(8)],  # IO Name row
        ["IO Data"] + [int(bit) for bit in f"{io:08b}"],  # IO Data row (binary)
        ["IO Mode"] + [int(bit) for bit in f"{io_modes:08b}"],  # IO Mode row (binary)
    ]

    # Format the row data into a table using DoubleTable class
    table = DoubleTable(rows)
    table.inner_row_border = True  # Enable inner row borders
    return table.table  # Return the formatted table string


def adc_io_display_on_lcd(
    sensors: OnBoardSensors,
    screen: Screen,
    interval: float = 0.01,
    adc_labels: Dict[int, str] = None,
    io_labels: Dict[int, str] = None,
):
    """
    Reads sensor values from ADC and IO channels and displays them on the screen.

    Args:
        sensors: An instance of the `OnBoardSensors` class.
        screen: An instance of the `Screen` class.
        interval (float, optional): The time interval between sensor readings in seconds. Defaults to 0.01.
        adc_labels (Dict[int, str], optional): A dictionary mapping ADC channel indices to custom labels. Defaults to None.
        io_labels (Dict[int, str], optional): A dictionary mapping IO channel indices to custom labels. Defaults to None.

    Returns:
        None

    Raises:
        KeyboardInterrupt: If the user interrupts the program by pressing Ctrl+C.
    """

    screen.set_font_size(FontSize.FONT_6X8)
    adc_labels = adc_labels or {}
    io_labels = io_labels or {}
    adc = sensors.adc_all_channels()
    # 打印 ADC 通道值表格
    for i in range(9):
        label = adc_labels.get(i, f"[{i}]")
        value = adc[i]
        screen.put_string(0, i * 8, f"{label}:{value}")

    io = [int(bit) for bit in f"{sensors.io_all_channels():08b}"]
    # 打印 IO 通道值表格
    for i in range(8):
        label = io_labels.get(i, f"[{i}]")
        value = io[i]
        screen.put_string(90, i * 8, f"{label}:{value}")
    screen.fill_screen(Color.BLACK).refresh()
    time.sleep(interval)
