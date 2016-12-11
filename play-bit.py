#!/usr/bin/env python
import sys
import subprocess
import math
import atexit

song, tempo, bit, command = sys.argv[1:]
bit = int(bit)
tempo = float(tempo)

def kill_process(pid):
    print "Killing pid={}".format(pid)
    os.kill(pid, signal.SIGTERM)

def get_song_length(name):
    output = subprocess.check_output(["sox", "--i", "-D", name])
    return float(output.rstrip())

def play(track_name, tempo, start_at, end_at):
    args = map(str, ["play", track_name, "trim", start_at, end_at, command, tempo,
        "repeat", "-"])
    p = subprocess.Popen(args)
    atexit.register(kill_process, p.pid)
    p.wait()


length = get_song_length(song)
max_length_snip = 15 # Each piece will last 30 secs
snips = math.ceil(length / max_length_snip)


start_at = (bit - 1) * max_length_snip
print "Playing bit {}/{}".format(bit, snips)
print "Start={}. Length={}".format(start_at, max_length_snip)

play(song, tempo, start_at, max_length_snip)
