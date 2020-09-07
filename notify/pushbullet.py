import sys
import traceback

import appdaemon.plugins.hass.hassapi as hass
from asyncpushbullet import AsyncPushbullet, InvalidKeyError, PushbulletError


class Pushbullet(hass.Hass):

    async def initialize(self):

        API_KEY = self.args['api_key']
        await self.register_endpoint(self.handle_request, self.args['endpoint'])

        EXIT_INVALID_KEY = 1
        EXIT_PUSHBULLET_ERROR = 2
        EXIT_OTHER = 3

        try:
            async with AsyncPushbullet(API_KEY) as pb:
                devices = await pb.async_get_devices()
                print("Devices:")
                for dev in devices:
                    print("\t", dev)

                push = await pb.async_push_note(title="Success", body="I did it!")
                print("Push sent:", push)

        except InvalidKeyError as ke:
            print(ke, file=sys.stderr)
            return EXIT_INVALID_KEY

        except PushbulletError as pe:
            print(pe, file=sys.stderr)
            return EXIT_PUSHBULLET_ERROR

        except Exception as ex:
            print(ex, file=sys.stderr)
            traceback.print_tb(sys.exc_info()[2])
            return EXIT_OTHER

    async def handle_request(self, data):
        pass
