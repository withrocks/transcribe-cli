import click
from transcribe_cli.transcribe_svc import TranscribeService
import logging
import os



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _get_input(msg, available):
    print("Entering _get_input")
    while True:
        action = input(msg)
        print("Got action {}".format(action))
        if action in available:
            return action


@click.command()
@click.argument('path', required=True)
@click.option('--length', '-l', type=float, help='Length of each part')
@click.option('--part', '-p', help='Part to play. If neither this nor section is provided, '
                                   'plays the last part')
@click.option('--section', help='Section to play, e.g. 0:10.')
@click.option('--speed', '-s', type=float, help='Relative speed')
@click.option('--nopitch', is_flag=True, help='Pitch is not adjusted on lower/higher speed')
def main(path, length, part, section, speed, nopitch):
    """Transcribe audio text on the command line"""
    logging.debug("Current PID: {}".format(os.getpid()))
    transcribe_svc = TranscribeService.create()
    transcribe_svc.set_path(path)

    if section and part:
        raise click.ClickException("Only one of part and section should be provided")
    elif section:
        section = tuple(map(float, section.split(":")))
        if length:
            logger.warn("Both length and section were provided. The length will be ignored.")
    elif part:
        if not length:
            length = 5
        section = transcribe_svc.get_section_from_part(int(part), length)
    else:
        # Neither part nor section was provided, figure out the last part from the metafile
        # defaulting the length if needed
        section = transcribe_svc.next_section(length)

    while True:
        transcribe_svc.play_section(section, speed, nopitch)
        print("Current speed: {}. Part: {}".format(speed, part))
        action = _get_input("Action: (n)ext bit, (q)uit, (s)lower, (f)aster ", "nqsf")
        if action == "n":
            length = section[1] - section[0]
            section = section[0] + length, section[1] + length
        elif action == "s":
            speed -= 0.1
        elif action == "f":
            speed += 0.1
        else:  # quit
            break

