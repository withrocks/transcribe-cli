# Trancsribe CLI

Command line interface for transcribing text, e.g. to aid understanding of a foreign language. 

Requirements:
 - Currently (while prototyping) requires sox: http://sox.sourceforge.net

   $ brew install sox

Install:
$ pip install -e .


Usage examples:

# Split the audio file into 10s segments, then play the 3rd segment. This will automatically
# repeat the segment 
`transcribe-cli --part 3 --length 10 ./audio.mp3`

# ... do the same, but slow the segment down to 80% (same pitch)
`transcribe-cli --part 3 --length 10 --speed 0.8 ./audio.mp3`
