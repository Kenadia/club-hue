import json
import random
import requests
from time import sleep, time
from collections import namedtuple

IP = '192.168.4.104'
BASE_URL = 'http://%s/api/kenschiller/' % IP


def set_light(light_id, color=None, bri=None, t=0):
    data = {
        'on': True,
        'xy': color,
        'bri': bri,
        'transitiontime': t
    }
    url = '%slights/%d/state' % (BASE_URL, light_id)
    requests.put(url, data=json.dumps(data))


Context = namedtuple('Context', ['timer', 'lights', 'colors'])


class Timer(object):

    def __init__(self, bpm):
        self.last_start_time = time()
        self.bpm = bpm

    def _wait(self):
        sleep(0.005)

    def wait_beats(self, beats):
        wait_end_time = self.last_start_time + (60.0 / self.bpm * beats)
        while time() < wait_end_time:
            self._wait()
            wait_end_time = self.last_start_time + (60.0 / self.bpm * beats)
        self.last_start_time = time()


class Lights(object):

    def __init__(self, light_ids):
        self.light_ids = light_ids

    def random_light(self):
        return random.choice(self.light_ids)

    def random_other_light(self, light_id):
        other_id = random.randint(0, len(self.light_ids) - 2)
        if other_id <= light_id:
            other_id += 1
        return other_id


class Colors(object):
    red = [6.7500E-01, 3.2200E-01]
    yellow = [5.4200E-01, 4.2000E-01]
    lime = [4.0900E-01, 5.1800E-01]
    pale = [2.8800E-01, 2.7900E-01]
    blue = [1.6700E-01, 4.0000E-02]
    pink = [4.2100E-01, 1.8100E-01]
    violet = [2.75E-01, 1E-01]

    def random_color(self, colors):
        r = random.random()
        rr = 1 - r
        new_color = [rr * colors[0][0] + r * colors[1][0],
                     rr * colors[0][1] + r * colors[1][1]]
        if len(colors[0]) == 2:
            return new_color
        else:
            return map(int,
                       new_color + [rr * colors[0][2] + r * colors[1][2]])


class Playable(object):

    def __init__(self, context):
        self.context = context
        self.timer = context.timer
        self.lights = context.lights
        self.colors = context.colors


class Action(Playable):
    '''Playable with a fixed duration.'''

    def __init__(self, context, beats):
        super(Action, self).__init__(context)
        self.beats = beats

    def play(self):
        self.timer.wait_beats(self.beats)


class LightAction(Action):
    '''Action with a light ID and params.'''

    def __init__(self, context, beats, light_id):
        super(LightAction, self).__init__(context, beats)
        self.light_id = light_id


class Dance(Playable):
    duration = float('inf')

    def __init__(self, context):
        super(Dance, self).__init__(context)
        self.sequences = [ClubLights(context, [Colors.red, Colors.yellow])]

    def play(self):
        while True:
            random.choice(self.sequences).play()


class ClubLights(Playable):
    skip_rate = 0.5
    beats_per_flash = 0.5
    flash_count = 64
    transition = 6
    duration = flash_count * beats_per_flash

    def __init__(self, context, color_source):
        super(ClubLights, self).__init__(context)
        self.color_source = color_source

    def play(self):
        light_id = self.lights.random_light()
        skipped_last = False

        for i in xrange(ClubLights.flash_count):
            should_flash = (
                skipped_last or i == ClubLights.flash_count - 1
                or random.random() > ClubLights.skip_rate)

            if should_flash:
                skipped_last = False
                color = self.colors.random_color(self.color_source)
                ClubLightsFlash(self.context, ClubLights.beats_per_flash,
                                light_id, color, ClubLights.transition).play()
                light_id = self.lights.random_other_light(light_id)
            else:
                skipped_last = True
                Action(self.context, beats=ClubLights.beats_per_flash).play()


class ClubLightsFlash(LightAction):

    def __init__(self, context, beats, light_id, color, transition):
        super(ClubLightsFlash, self).__init__(context, beats, light_id)
        self.color = color
        self.transition = transition

    def play(self):
        set_light(self.light_id, color=self.color, bri=255)
        set_light(self.light_id, bri=0, t=self.transition)
        super(ClubLightsFlash, self).play()
