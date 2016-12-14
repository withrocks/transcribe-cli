import os
import logging
from transcribe_cli.file_svc import FileService
from transcribe_cli.sound import SoundPlayer
import re


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
        self.metafile = None
        self.path = None
        self.section = None

    def next_section(self, length):
        # TODO: Algorithm to find continuous stretches. Cheat for now and
        # just find the highest `to` value (that strategy may miss parts)
        largest = (0, 0)
        for key in self.metafile["lines"]:
            start_at, end_at = map(int, key.split(":"))
            if end_at > largest[1]:
                largest = start_at, end_at
        if not length:
            length = largest[1] - largest[0]
        return largest[1], largest[1] + length  # TODO: bounds

    def set_path(self, path):
        # Set the current path, will load the metafile
        self.path = path
        self.metafile = self.file_service.get_metafile(path)

    def get_section_from_part(self, part, length):
        end_at = (part * length)
        start_at = end_at - length
        return start_at, end_at

    def play_section(self, section, speed, nopitch):
        if not self.path:
            raise ValueError("Path has not been set")
        start_at, end_at = section
        length = end_at - start_at
        last_line_key = "{}:{}".format(start_at, end_at)
        try:
            last_line = self.metafile["lines"][last_line_key]
        except:
            last_line = ""

        # Also, add all other lines that involve the same part of the file, i.e.
        # start_at or end_at is within those bounds

        def get_related():
            for key in self.metafile["lines"]:
                if key == last_line_key:
                    continue
                other_start_at, other_end_at = map(int, key.split(":"))
                if start_at <= other_start_at <= end_at or\
                   start_at <= other_end_at <= end_at:
                    yield other_start_at, other_end_at

        file_buffer = list()
        file_buffer.append(last_line)

        for start_at_current, end_at_current in sorted(get_related()):
            key = "{}:{}".format(start_at_current, end_at_current)
            file_buffer.append("!{}: {}".format(key, self.metafile["lines"][key]))

        file_buffer = os.linesep.join(file_buffer)

        # Start playing, this will automatically exit
        self.sound_player.play(self.path, speed, start_at, length, nopitch)
        new_content = self.file_service.edit_temp_file(bytes(file_buffer, encoding="UTF-8"))
        # Filter out comments and lines starting with exclamation points
        # The latter will be processed further later.
        updated = self._parse_update(new_content, last_line_key)
        self.sound_player.stop()

        # Update the metafile:
        update_count = 0
        for key in updated:
            if updated[key] == "":
                # Ignore empty lines
                continue
            if key not in self.metafile["lines"] or self.metafile["lines"][key] != updated[key]:
                update_count += 1
                self.metafile["lines"][key] = updated[key]

        if update_count > 0:
            self.file_service.save_metafile(self.metafile)
            self.logger.info("Saved metafile")
        else:
            self.logger.info("No updates, not saving metafile")

    def _parse_update(self, input_file, current_clip):
        """
        The beginning of the file, if there is no prefix, is considered
        to be part of the current clip. Comments will be ignored (starting with #)

        If a line starts with "!" it changes the state to another segment range, which should
        follow directly after it. Everything following that line will be considered to be part
        of that clip (comments also being ignored).
        """
        # NOTE: Totally non-optimized
        ret = dict()
        clip = current_clip
        ret[clip] = list()

        for line in input_file.splitlines():
            print("HERE", line)
            if line.startswith("#"):
                continue
            elif line.startswith("!"):
                # Change state
                match = re.match(r"^!(\d+:\d+):(.*)", line)
                # If this is not a match, it will be added as part of the earlier clip
                if match:
                    clip = match.group(1)
                    line = match.group(2).lstrip()
                    ret[clip] = list()
            #print("appending", clip, line)
            ret[clip].append(line)
        for key, value in ret.items():
            ret[key] = "\n".join(value)
        return ret

    @staticmethod
    def create():
        sound_player = SoundPlayer()
        file_service = FileService()
        return TranscribeService(sound_player, file_service)
