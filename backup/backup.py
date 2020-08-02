import mqttapi as mqtt
from ping3 import ping
import datetime

class Backup(mqtt.Mqtt):

    def initialize(self):
        self.log('initializing backup script')

        time = datetime.time(0, 0, 0)
        self.run_minutely(self.check_primary, time)

    def check_primary(self, kwargs):
        try:
            primary_host = ping('192.168.2.13')

            # check if the primary home assistant is up.  If not, restart it
            if not primary_host:
                self.log('Home assistant is down')
                #self.turn_off('switch.home_assistant')

                #self.turn_on('switch.home_assistant')
        except Exception as ex:
            print(ex)

#    def toggle_primary(self):


