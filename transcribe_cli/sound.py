import atexit
import subprocess
import os
import signal
import math
import logging


class SoundPlayer(object):
    def __init__(self, logger=None):
        self.parts = None
        self.part = None
        self._process = None
        self.start_at = None
        self.end_at = None
        self.total_length = None
        self.part_length = None
        self.speed = None
        self.nopitch = None
        self.logger = logger or logging.getLogger(__name__)

    def play(self, sound_file, speed, start_at, length, nopitch):
        speed_action = "speed" if nopitch else "tempo"
        start_at = max(0, start_at - 0.1)  # start 0.1 second before
        args = list(map(str, ["play", sound_file,
                    "trim", start_at, length,
                    speed_action, speed,
                    "pad", "0", "0.8",
                    "repeat", "-"]))
        logging.debug("Starting play process with args: {}".format(args))
        FNULL = open(os.devnull, 'w')
        p = subprocess.Popen(args, stdout=FNULL, stderr=subprocess.STDOUT)
        self._process = p
        print("Started sound process {}".format(self._process.pid))
        # Register for process destruction, if the caller forgets to call stop
        #atexit.register(self._kill_process)

    def stop(self):
        self._kill_process()
        self._process = None

    def get_length(self, sound_file):
        output = subprocess.check_output(["sox", "--i", "-D", sound_file])
        return float(output.rstrip())

    def _kill_process(self):
        if self._process is not None:
            print("Killing process {}".format(self._process))
            os.kill(self._process.pid, signal.SIGTERM)
            retcode = self._process.wait()  # TODO: Unix only
            print("Done waiting for sound process. retcode={}".format(retcode))
            self._process = None

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
