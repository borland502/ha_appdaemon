import datetime

import appdaemon.plugins.hass.hassapi as hass


class HvacSchedule(hass.Hass):

    # initialize() function which will be called at startup and reload
    def initialize(self):

        time = datetime.time(20, 0, 0)
        # Schedule a daily callback that will call run_daily() at 10:44 pm every night
        self.run_daily(self.turn_unit_on_c, time)

        # turn off at 8:00 am every morning
        time = datetime.time(8, 0, 0)
        self.run_daily(self.turn_unit_off_c, time)

    def turn_unit_on_c(self, kwargs):
        try:
            self.log("Turning on Bedroom AC")

            # Call to Home Assistant to turn the AC on
            self.call_service(
                "switch/turn_on",
                entity_id="switch.bedroom_ac"
            )

        except Exception as ex:
            self.log(str(ex))

    def turn_unit_off_c(self, kwargs):
        self.log("Turning off Bedroom AC")

        # Call to Home Assistant to turn the AC on
        self.call_service(
            "switch/turn_off",
            entity_id="switch.bedroom_ac"
        )
