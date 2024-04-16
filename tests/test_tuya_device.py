import unittest
from tuya_utils.tuya_device import TuyaDevice
from pprint import pprint

# Set up device_id
power_strip_devices = [
    {"name": "Serj", "id": "eb59e004fffa45fd96bpn2"},
    {"name": "Dan", "id": "eb56a18d587d32124djrkd"}
]

smart_plug_devices = [
    {"name": "circle1", "id": "ebebd4217833a3782egehr"},
    {"name": "brick1", "id": "eb3a591fd3b3589037v7am"}
]


class TestTuyaDevice(unittest.TestCase):
    def test_describe_device(self):
        device = TuyaDevice()
        device_id = power_strip_devices[1]["id"]
        response = device.get_device_info(device_id)
        pprint(response)
        self.assertEqual(True, True)  # add assertion here

    def test_device_status(self):
        device = TuyaDevice()
        device_id = power_strip_devices[1]["id"]
        response = device.get_device_status(device_id)
        pprint(response)
        self.assertEqual(True, True)

    def test_set_switch_on(self):
        device = TuyaDevice()
        device_id = power_strip_devices[1]["id"]
        response = device.set_switch_power(device_id, 1, True)
        pprint(response)
        self.assertEqual(True, True)

    def test_set_switch_off(self):
        device = TuyaDevice()
        device_id = power_strip_devices[1]["id"]
        response = device.set_switch_power(device_id, 1, False)
        pprint(response)
        self.assertEqual(True, True)

    # TODO:
    #  - Figure out light schedule: get and set
    #  - Create function to turn off all switches at once


if __name__ == '__main__':
    unittest.main()
