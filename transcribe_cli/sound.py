import atexit
import subprocess
import os
import signal
import math


class SoundPlayer(object):
    def __init__(self):
        self.parts = None
        self.part = None
        self._process = None
        self.start_at = None
        self.end_at = None
        self.total_length = None
        self.part_length = None
        self.speed = None
        self.nopitch = None

    def play(self, sound_file, speed, start_at, length, nopitch):
        speed_action = "speed" if nopitch else "tempo"
        args = map(str, ["play", sound_file, "trim", start_at, length, speed_action, speed,
                         "repeat", "-"])
        FNULL = open(os.devnull, 'w')
        p = subprocess.Popen(args, stdout=FNULL, stderr=subprocess.STDOUT)
        self._process = p.pid
        # Register for stop, if the caller forgets to call stop
        atexit.register(self._kill_process)

    def stop(self):
        self._kill_process()
        self._process = None

    def get_length(self, sound_file):
        output = subprocess.check_output(["sox", "--i", "-D", sound_file])
        return float(output.rstrip())

    def _kill_process(self):
        if self._process is not None:
            os.kill(self._process, signal.SIGTERM)

    def play_part(self):
        self.play(self.sound_file, self.speed, self.start_at, self.part_length, self.nopitch)

    def set_part(self, sound_file, part, part_length, speed, nopitch):
        self.sound_file = sound_file
        self.total_length = self.get_length(sound_file)
        self.part = part
        self.parts = math.ceil(self.total_length / part_length)
        self.part_length = part_length
        self.start_at = int((part - 1) * self.part_length)
        self.end_at = self.start_at + self.part_length
        self.speed = speed
        self.nopitch = nopitch


