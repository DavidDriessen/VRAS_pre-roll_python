from splash import splash
from moviepy.editor import *
import subprocess
import glob
from pathlib import Path
from random import shuffle
import os

def clean_dir(dir):
    files = glob.glob(dir + "/*", recursive=True)
    for file in files:
        os.remove(file)
        pass
    pass
clean_dir('./output/splash/')
clean_dir('./output/Trailers/')
clean_dir('./output/tmp/')


# Stage 1 generating still frame 
splash().save_frame('./output/posters.png')

# Stage 2 Overlaying trailers over still frame
for trailer in glob.glob('Trailers/*.mp4'):
    subprocess.call(["ffmpeg", "-i", "./output/posters.png", "-i", "./{0}".format(trailer), "-filter_complex", "[1:0]scale=900:506,setsar=1[a];[0:0][a] overlay=1020:574", "-map", "1:a", "-shortest", "-y", "./output/{0}".format(trailer)])
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

    cmd = ["magick","convert","./output/posters.png","-gravity","center","-fill","white","-pointsize","40","-font","Arial","-annotate","+480+40","This session:\n" + " & ".join(current), "./output/tmp/text.png"]
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

    cmd = ["ffmpeg", "-f","lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-loop", "1", "-i", os.path.realpath(splash), "-c:v", "libx264", "-t", "10", "-pix_fmt", "yuv420p", "-vf", "scale=1920:1080", "-y", "./output/tmp/splash.mp4"]
    p = subprocess.Popen(cmd)
    p.wait()

    g = glob.glob("./output/Trailers/*")
    shuffle(g)
    for trailer in g:
        p = Path(trailer)
        current_trailer = p.stem
        # Don't want to show a trailer of the show that we're currently showing
        if current_trailer in current_session:
            print("Not showing " + current_trailer + " because current session is " + "+".join(current_session))
            continue
        concat_list.append(  trailer.replace("\\","/") )
        concat_list.append( './output/tmp/splash.mp4') 
        
        pass
    filter=""
    i=0
    length=0
    cmd = ["ffmpeg"]
    for video in concat_list:
        filter = filter + "[{0}:v] [{0}:a]".format(i)
        cmd.append("-i")
        cmd.append(video)
        
        process = subprocess.Popen(["ffprobe", "-loglevel", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", video],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = process.communicate()
        length = length + float(out[0])

        i+=1
        
        pass
    filter = filter + " concat=n={0}:v=1:a=1 [b] [a]; [b] drawtext=fontfile=OpenSans-Regular.ttf:text='%{{eif\\:trunc(mod((({1}-t)/60),60))\\:d\\:2}}\\:%{{eif\\:trunc(mod({1}-t\\,60))\\:d\\:2}}':fontcolor=white:fontsize=24:x=w-tw-10:y=h-th-10:box=1:boxcolor=black@0.5:boxborderw=10,format=yuv420p [v]".format(len(concat_list), length)
    cmd = cmd + ["-filter_complex",filter,"-map","[v]","-map","[a]","-y","./output/00 {}.mp4".format("+".join(current_session))]
    print(" ".join(cmd))
    p = subprocess.Popen(cmd)
    p.wait()
    pass
