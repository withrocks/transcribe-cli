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
@click.option('--length', '-l', default=5, help='Length of each part')
@click.option('--part', '-p', default=1, help='Part to play')
@click.option('--speed', '-s', help='Relative speed')
@click.option('--nopitch', is_flag=True, help='Pitch is not adjusted on lower/higher speed')
@click.argument('path', required=True)
def main(path, length, part, speed, nopitch):
    """Transcribe audio text on the command line"""
    logging.debug("Current PID: {}".format(os.getpid()))
    transcribe_svc = TranscribeService.create()

    while True:
        transcribe_svc.play_part(path, part, length, speed, nopitch)
        action = _get_input("Action: (n)ext bit, (q)uit: ", "nq")
        if action == "n":
            part += 1
        else:  # quit
            break
