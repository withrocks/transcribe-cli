import os
import yaml
import click
from transcribe_cli.sound import SoundPlayer
from transcribe_cli.file_svc import FileService


@click.command()
@click.option('--length', '-c', default=5, help='Length of each part')
@click.option('--part', '-p', default=1, help='Part to play')
@click.option('--speed', '-s', help='Relative speed')
@click.option('--nopitch', is_flag=True, help='Pitch is not adjusted on lower/higher speed')
@click.argument('path', required=True)
def main(path, length, part, speed, nopitch):
    """Transcribe audio text on the command line"""

    file_svc = FileService()
    file_svc.read_metafile(path)  # Returns the metafile (dict) corresponding to the audio file

    directory, fname = os.path.split(path)
    fname_no_ext, ext = os.path.splitext(fname)
    assert ext != ".yaml"  # Can never be too sure
    metapath = os.path.join(directory, fname_no_ext + ".yaml")

    try:
        with open(metapath) as fs:
            metafile = yaml.load(fs)
    except FileNotFoundError:
        metafile = {"path": path, "lines": dict()}


    player = SoundPlayer()
    player.set_part(path, part, length, speed, nopitch)
    print("Part {}/{}".format(player.part, player.parts))
    key = "{}:{}".format(player.start_at, player.end_at)
    try:
        last_line = metafile["lines"][key]
    except:
        last_line = ""

    # Start playing, this will automatically exit
    player.play_part()
    new_content = file_svc.edit_temp_file(bytes("{}".format(last_line),
                                                encoding="UTF-8"))
    player.stop()
    metafile["lines"][key] = new_content
    with open(metapath, "w") as fs:
        yaml.dump(metafile, fs, default_flow_style=False)

