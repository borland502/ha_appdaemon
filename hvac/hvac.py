import appdaemon.plugins.hass.hassapi as hass
import datetime


class HvacSchedule(hass.Hass):

    # initialize() function which will be called at startup and reload
    def initialize(self):

        time = datetime.time(20, 44, 0)
        # Schedule a daily callback that will call run_daily() at 10pm every night
        self.run_daily(self.run_daily_callback, time)

    # Our callback function will be called by the scheduler every day at 7pm
    def run_daily_callback(self, kwargs):
        try:
            self.log("Turning on Bedroom AC")

            # Call to Home Assistant to turn the porch light on
            self.call_service(
                "switch/turn_on",
                entity_id="switch.bedroom_ac"
            )

        except Exception as ex:
            self.log(ex)