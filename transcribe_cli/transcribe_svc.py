from transcribe_cli.file_svc import FileService
from transcribe_cli.sound import SoundPlayer


class TranscribeService(object):
    def __init__(self, sound_player, file_service):
        self.sound_player = sound_player
        self.file_service = file_service

    def play_part(self, path, part, length, speed, nopitch):
        metafile = self.file_service.get_metafile(path)
        # TODO: the sound player contains unecessary logic
        self.sound_player.set_part(path, part, length, speed, nopitch)
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
        self.sound_player.stop()
        metafile["lines"][key] = new_content
        print("Saving metafile")
        self.file_service.save_metafile(metafile)
        print("Saved metafile")

    @staticmethod
    def create():
        sound_player = SoundPlayer()
        file_service = FileService()
        return TranscribeService(sound_player, file_service)
