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
for session in glob.glob('Sessions/*'):
    poster_array = []
    current = []
    for poster in glob.glob(session):
        poster_array.append(poster)

        name = poster.split(".")[-2]
        current.append(name)

        subprocess.call("convert {} -resize 320x450! ./output/tmp/{}.png".format(poster, name))
        pass
    subprocess.call("convert {} +append ./output/tmp/lineup.png".format(" ".join(poster_array)))
    subprocess.call("convert ./output/posters.png -gravity center -fill white -pointsize 40 -font Helvetica -annotate +480+40 '{}' ./output/tmp/text.png".format(" & ").join(current))
    subprocess.call("convert ./output/tmp/text.png ./output/tmp/lineup.png -gravity center -geometry +480+315 -composite ./output/splash/{}.png".format("+".join(current)))
    
# Stage 4 concatenating stage 2 + 3