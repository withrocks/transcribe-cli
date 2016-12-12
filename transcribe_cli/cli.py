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
@click.option('--part', '-p', help='Part to play. If not supplied, finds the last part.')
@click.option('--speed', '-s', help='Relative speed')
@click.option('--nopitch', is_flag=True, help='Pitch is not adjusted on lower/higher speed')
@click.argument('path', required=True)
def main(path, length, part, speed, nopitch):
    """Transcribe audio text on the command line"""
    logging.debug("Current PID: {}".format(os.getpid()))
    transcribe_svc = TranscribeService.create()
    speed = float(speed)
    part = int(part)

    while True:
        transcribe_svc.play_part(path, part, length, speed, nopitch)
        print("Current speed: {}. Part: {}".format(speed, part))
        action = _get_input("Action: (n)ext bit, (q)uit, (s)lower, (f)aster ", "nqsf")
        if action == "n":
            part = transcribe_svc.part + 1
        elif action == "s":
            speed -= 0.1
        elif action == "f":
            speed += 0.1
        else:  # quit
            break

