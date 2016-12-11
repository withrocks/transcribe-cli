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

    def play(self, sound_file, tempo, start_at, length):
        args = map(str, ["play", sound_file, "trim", start_at, length, "tempo", tempo,
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

    def play_part(self, sound_file, part, part_length, tempo):
        total_length = self.get_length(sound_file)
        self.part = part
        self.parts = math.ceil(total_length / part_length)
        start_at = int((part - 1) * total_length)
        self.play(sound_file, tempo, start_at, part_length)

