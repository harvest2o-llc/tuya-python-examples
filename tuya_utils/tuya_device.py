import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
import os
from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ACCESS_ID = os.getenv("TUYA_ACCESS_ID")
ACCESS_KEY = os.getenv("TUYA_ACCESS_KEY")
API_ENDPOINT = os.getenv("TUYA_API_ENDPOINT")

# https://developer.tuya.com/en/docs/iot/switch-socket-and-power-strip?id=K9gf7o3qbbklt
# Timers: https://developer.tuya.com/en/docs/cloud/timing-management?id=K95zu050h5m53

"""
These aer all timing events that are sent to the Tuya device. The device will turn on or off based on the time and the dps value.

"TYPE":"CREATE", "id":486452190, "time":"19:00", "dps":"false", "loops":"1111111", "status":"opened", "Notification":false

"TYPE":"CREATE", "id":486446512, "time":"06:00", "dps":"true", "loops":"1111111", "status":"opened", "Notification":false

"TYPE":"DELETED", "id":486446512, "time":"06:00", "dps":"true", "loops":"1111111", "status":"deleted", "Notification":false

"TYPE":"CREATE", "id":486438883, "time":"06:15", "dps":"true", "loops":"1111111", "status":"opened", "Notification":false

Setting schedule and then waiting does not show a message from server, only from device, so not stored on server
Also, I do not see it in default data fromm device status... so stored elsewhere


"""


class TuyaDevice:
    openapi = None

    def __init__(self):
        TUYA_LOGGER.setLevel(logging.ERROR)
        self.openapi = self.tuya_connect()

    def tuya_connect(self):
        # Enable debug log

        # Init OpenAPI and connect
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        return openapi

    def get_device_info(self, device_id):
        response = self.openapi.get("/v1.0/iot-03/devices/{}".format(device_id))
        return response

    def get_device_commands(self, device_id):
        response = self.openapi.get("/v1.0/iot-03/devices/{}/functions".format(device_id))
        return response

    def set_switch_power(self, device_id, switch_number, value):
        commands = {'commands': [{'code': f'switch_{switch_number}', 'value': value}]}
        response = self.openapi.post('/v1.0/iot-03/devices/{}/commands'.format(device_id), commands)
        return response

    def get_device_status(self, device_id):
        response = self.openapi.get("/v1.0/iot-03/devices/{}/status".format(device_id))
        return response

    # function to turn off switches 1 through 4 with a single command
    def turn_off_all_switches(self, device_id):
        commands = {'commands': [{'code': 'switch_1', 'value': False},
                                 {'code': 'switch_2', 'value': False},
                                 {'code': 'switch_3', 'value': False},
                                 {'code': 'switch_4', 'value': False}]}
        response = self.openapi.post('/v1.0/iot-03/devices/{}/commands'.format(device_id), commands)
        return response

    def get_device_timers(self, device_id):
        # https://developer.tuya.com/en/docs/cloud/timing-management?id=K95zu050h5m53
        response = self.openapi.get("/v1.0/devices/{}/timers".format(device_id))
        return response

    def delete_all_timers(self, device_id):
        # https://developer.tuya.com/en/docs/cloud/timing-management?id=K95zu050h5m53
        response = self.openapi.delete("/v1.0/devices/{}/timers".format(device_id))
        return response

    def create_timer(self, device_id, start_time):
        # https://developer.tuya.com/en/docs/cloud/timing-management?id=K95zu050h5m53
        timer = {
            "instruct": [
                {
                    "functions": [
                        {
                            "code": "switch_1",
                            "value": True
                        }
                    ],
                    "date": "00000000",
                    "time": start_time
                }
            ],
            "loops": "1111111",
            "category": "test",
            "timezone_id": "America/Chicago",
            "time_zone": "-6:00"
        }

        response = self.openapi.post("/v1.0/devices/{}/timers".format(device_id), timer)
        return response

    def get_end_time(self, start_time, duration_minutes):
        # Parse the start_time string into a datetime object
        time_format = "%H:%m"
        time_obj = datetime.strptime(start_time, "%H:%M")

        # Create a timedelta object for the duration
        duration = timedelta(minutes=duration_minutes)

        # Add the duration to the start time
        end_time_obj = time_obj + duration

        # Format the end time back to string, using only the hour and minute parts
        end_time = end_time_obj.strftime("%H:%M")

        return end_time

    def create_rise_garden_timer(self, device_id, start_time, duration_minutes):
        # Assume there are 4 switches that will all be scheduled to be the same
        # category will include all the switches in one group - to be named "rise_garden"
        # First all timers will be deleted for the device and then the new timer will be created
        # then create a timer for each switch in a single API call
        end_time = self.get_end_time(start_time, duration_minutes)
        timer = {
            "instruct": [
                {
                    "functions": [
                        {
                            "code": "switch_1",
                            "value": True
                        },
                        {
                            "code": "switch_2",
                            "value": True
                        },
                        {
                            "code": "switch_3",
                            "value": True
                        },
                        {
                            "code": "switch_4",
                            "value": True
                        }
                    ],
                    "date": "00000000",
                    "time": start_time
                },
                {
                    "functions": [
                        {
                            "code": "switch_1",
                            "value": False
                        },
                        {
                            "code": "switch_2",
                            "value": False
                        },
                        {
                            "code": "switch_3",
                            "value": False
                        },
                        {
                            "code": "switch_4",
                            "value": False
                        }
                    ],
                    "date": "00000000",
                    "time": end_time
                }
            ],
            "loops": "1111111",
            "category": "rise_garden",
            "timezone_id": "America/Chicago",
            "time_zone": "-6:00"
        }

        response = self.openapi.delete("/v1.0/devices/{}/timers".format(device_id))
        print(response)

        response = self.openapi.post("/v1.0/devices/{}/timers".format(device_id), timer)
        print(response)

        return response


    # def delete_timer_category(self, device_id, category):
    #     # https://developer.tuya.com/en/docs/cloud/timing-management?id=K95zu050h5m53
    #     response = self.openapi.delete("/v1.0/devices/{}/timers/{}".format(device_id, category))
    #     return response