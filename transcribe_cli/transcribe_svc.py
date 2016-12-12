import os
import logging
from transcribe_cli.file_svc import FileService
from transcribe_cli.sound import SoundPlayer


"""
# You have this:
0-5:    a
5-10:   b
        # missing
10-15   d


# You then execute 0-15 and get:
0-15:   a | b | # | d

    editing this string (and removing pipes) would lead to those being merged

# if you would execute 2-7, you should get something like:
2-7:    a | b

    editing this would not lead to a merge

"""


class TranscribeService(object):
    def __init__(self, sound_player, file_service, logger=None):
        self.sound_player = sound_player
        self.file_service = file_service
        self.logger = logger or logging.getLogger(__name__)

    def next_part(self, metafile, length):
        # TODO: Algorithm to find continuous stretches. Cheat for now and
        # just find the highest to value (that strategy may miss parts)
        largest = 0
        for key in metafile["lines"]:
            _, to = map(int, key.split(":"))
            if to > largest:
                largest = to
        return int(largest / length) + 1

    def play_part(self, path, part, length, speed, nopitch):
        metafile = self.file_service.get_metafile(path)

        self.part = part
        if self.part is None:
            self.part = self.next_part(metafile, length)

        # TODO: the sound player contains logic it shouldn't need to know
        self.sound_player.set_part(path, self.part, length, speed, nopitch)
        print("Progress: {}".format(float(self.sound_player.part) /
              self.sound_player.parts))
        key = "{}:{}".format(self.sound_player.start_at, self.sound_player.end_at)
        try:
            last_line = metafile["lines"][key]
        except:
            last_line = ""

        # Start playing, this will automatically exit
        self.sound_player.play_part()
        new_content = self.file_service.edit_temp_file(bytes("{}".format(last_line),
                                                       encoding="UTF-8"))
        # Filter out comment lines:
        os.linesep
        filtered = os.linesep.join(line for line in new_content.splitlines()
                                   if not line.startswith("#"))
        filtered = filtered.strip()

        self.sound_player.stop()
        metafile["lines"][key] = filtered
        if filtered != "":
            self.file_service.save_metafile(metafile)
            self.logger.info("Saved metafile")
        else:
            self.logger.info("Empty content, not saving entry")

    @staticmethod
    def create():
        sound_player = SoundPlayer()
        file_service = FileService()
        return TranscribeService(sound_player, file_service)
