from splash import splash
from moviepy.editor import *
import subprocess
import glob

# Stage 1 generating still frame 
splash().save_frame('./output/posters.png')

# Stage 2 Overlaying trailers over still frame
for trailer in glob.glob('Trailers/*.mp4'):
    subprocess.call("ffmpeg -i ./output/posters.png -i ./{0} -filter_complex \"[1:0]scale=900:506,setsar=1[a];[0:0][a] overlay=1020:574\" -map 1:a -shortest -y ./output/{0}".format(trailer))
    pass
# Stage 3 generating still frame with current session poster

# Stage 4 concatenating stage 2 + 3