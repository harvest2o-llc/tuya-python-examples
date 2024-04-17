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

    def test_get_timers(self):
        device = TuyaDevice()
        device_id = power_strip_devices[1]["id"]
        response = device.get_device_timers(device_id)
        pprint(response)
        self.assertEqual(True, True)

    def test_delete_timers(self):
        device = TuyaDevice()
        device_id = power_strip_devices[1]["id"]
        response = device.delete_all_timers(device_id)
        pprint(response)
        self.assertEqual(True, True)

    def test_create_timer(self):
        device = TuyaDevice()
        device_id = power_strip_devices[1]["id"]
        response = device.create_timer(device_id, "06:00")
        pprint(response)
        self.assertEqual(True, True)

    # def test_delete_timer_category(self):
    #     device = TuyaDevice()
    #     device_id = power_strip_devices[1]["id"]
    #     response = device.delete_timer_category(device_id, "test")
    #     pprint(response)
    #     self.assertEqual(True, True)

    def test_set_rise_garden_schedule(self):
        device = TuyaDevice()
        device_id = power_strip_devices[1]["id"]
        response = device.create_rise_garden_timer(device_id, "07:00", 60*16)
        pprint(response)

        response = device.get_device_timers(device_id)
        pprint(response)

        self.assertEqual(True, True)

    # TODO:
    #  - Get schedule to show up in Tuya app
    #  - Create function to turn off all switches at once


if __name__ == '__main__':
    unittest.main()
