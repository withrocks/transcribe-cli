# Trancsribe CLI

Command line interface for transcribing text, e.g. to aid understanding of a foreign language. 

## Requirements:
Currently (while prototyping) requires sox: http://sox.sourceforge.net
- Mac: `brew install sox`

## Install:
`pip install -e .`
 
## Usage
### Transcribe voice audio
The following commands will all fire up vim for transcribing, while playing the audio clip in the background
```
# Split the audio file into 10s segments, then play the 3rd segment. This will automatically
# repeat the segment
transcribe-cli --part 3 --length 10 ./audio.mp3
```

```
# ... do the same as in the previous example, but slow the segment down to 80% (keeping the pitch unchanged)
transcribe-cli --part 3 --length 10 --speed 0.8 ./audio.mp3
```

When you quit vim, the transcription will be added to a metadata file (yaml extension), in the same directory as the audio file.

If you don't specify the segment, the application will go to the next unprocessed segment:
`transcribe-cli --length 10 ./audio.mp3`
