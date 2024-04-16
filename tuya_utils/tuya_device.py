import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ACCESS_ID = os.getenv("TUYA_ACCESS_ID")
ACCESS_KEY = os.getenv("TUYA_ACCESS_KEY")
API_ENDPOINT = os.getenv("TUYA_API_ENDPOINT")

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
