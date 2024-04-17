# tuya-python-examples
A repo to create and share more detailed examples of how to use the Tuya API with Python.
This is using the tuya-connector-python library found here:https://github.com/tuya/tuya-connector-python
It is not very active... so a bit suspect, but seems to work at the basic level


TODO:
Timers
- Array of categories (I think this will something like a group of schedules for a device component (i.e. switch)
- - groups, the actual timer schedules - on/off(function) triggers
- - - timer def (name, date, loops, order in group, status time, dimer_id, timezone, function (on/off switch)

Start off simple, set all timers to start at 7a and run for 16hrs
- function will delete all timers, then set them to the same



Helpful references
- Getting started ref: https://developer.tuya.com/en/demo/python-iot-development-practice
  Important note on this... They Smart Industry app is not longer supported. You need another way to provision devices into your account.
  We did this three ways 1) used a virtual device (not very satisfying), 2) registered devices in Smat Life app then linked the account 
  and 3) Created an app with the SDK, linked the app to the IoT project and paired devices from custom app.
- IoT Console - the debugging console can be useful 
