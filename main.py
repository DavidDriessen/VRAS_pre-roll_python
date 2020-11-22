from splash import splash
from moviepy.editor import *
import subprocess
import glob
from pathlib import Path
from random import shuffle
import os

# Stage 1 generating still frame 
splash().save_frame('./output/posters.png')

# Stage 2 Overlaying trailers over still frame
for trailer in glob.glob('Trailers/*.mp4'):
    #subprocess.call(["ffmpeg", "-i", "./output/posters.png", "-i", "./{0}".format(trailer), "-filter_complex", "[1:0]scale=900:506,setsar=1[a];[0:0][a] overlay=1020:574", "-map", "1:a", "-shortest", "-y", "./output/{0}".format(trailer)])
    pass
# Stage 3 generating still frame with current session poster
for session in glob.glob('Sessions/*'):
    poster_array = []
    current = []
    for poster in glob.glob(session + '/*'):
        p = Path(poster)
        name = p.stem
        current.append(name)
        poster_array.append("./output/tmp/{}.png".format(name))
        cmd = ["magick","convert",poster,"-resize","320x450!","./output/tmp/{}.png".format(name)]
        p = subprocess.Popen(cmd)
        p.wait()
        pass
    cmd = ["magick","convert"] + poster_array + ["+append","./output/tmp/lineup.png"]
    p = subprocess.Popen(cmd)
    p.wait()

    cmd = ["magick","convert","./output/posters.png","-gravity","center","-fill","white","-pointsize","40","-font","Arial","-annotate","+480+40"," & ".join(current), "./output/tmp/text.png"]
    p = subprocess.Popen(cmd)
    p.wait()

    cmd = ["magick","convert","./output/tmp/text.png","./output/tmp/lineup.png", "-gravity","center","-geometry","+480+315","-composite", "./output/splash/{}.png".format("+".join(current))]
    p = subprocess.Popen(cmd)
    p.wait()
# Stage 4 concatenating stage 2 + 3

for splash in glob.glob("./output/splash/*"):
    concat_list = []
    p = Path(splash)
    current_session = p.stem.split("+")

    cmd = ["ffmpeg", "-loop", "1", "-i", os.path.realpath(splash), "-c:v", "libx264", "-t", "10", "-pix_fmt", "yuv420p", "-vf", "scale=1920:1080", "-y", "./output/tmp/splash.mp4"]
    p = subprocess.Popen(cmd)
    p.wait()

    g = glob.glob("./output/Trailers/*")
    shuffle(g)
    for trailer in g:
        p = Path(trailer)
        current_trailer = p.stem
        # Don't want to show a trailer of the show that we're currently showing
        if current_trailer in current_session:
            continue
        concat_list.append( VideoFileClip( trailer.replace("\\","/") ) )
        concat_list.append( VideoFileClip('./output/tmp/splash.mp4') )
        
        pass
    print(concat_list)
    concat_clip = concatenate_videoclips(concat_list, method="compose") 
    concat_clip.write_videofile("./output/00 {}.mp4".format("+".join(current_session)))
    pass
