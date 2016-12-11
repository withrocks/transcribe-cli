import click
from transcribe_cli.sound import SoundPlayer
from transcribe_cli.file_svc import FileService
import os


@click.command()
@click.option('--length', '-c', default=5, help='Length of each part')
@click.option('--part', '-p', default=1, help='Part to play')
@click.option('--tempo', '-t', default=0.7, help='Tempo to play at')
@click.argument('path', required=True)
def main(path, length, part, tempo):
    """Transcribe audio text on the command line"""


    directory, fname = os.path.split(path)
    fname_no_ext, ext = os.path.splitext(fname)
    assert ext != ".txt"  # Can never be too sure
    metafile = os.path.join(directory, fname_no_ext + ".txt")
    if not os.path.exists(metafile):
        with open(metafile, "w"):
            pass
    print(metafile)

    file_svc = FileService()
    #file_svc.write_line(metafile, 10, "some shit")
    print(file_svc.read_line(metafile, 10))
    return
    last_line = file_svc.read_line(metafile, part)

    player = SoundPlayer()
    # Start playing, this will automatically exit
    #player.play_part(path, part, length, tempo)
    new_content = file_svc.edit_temp_file(bytes("{}".format(last_line),
                                                encoding="UTF-8"))
    #player.stop()
    print(new_content)
    #file_svc.write_line(new_content)




