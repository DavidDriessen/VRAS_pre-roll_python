import glob
from moviepy.editor import *
from splash import splash
from timer import add_timer

trailers = [VideoFileClip(t).resize((320, 500)).resize((1920, 1080)).fadein(1).fadeout(1)
            for t in glob.glob('Trailers/*.mp4')]

clips = [splash()]

for i in range(0, len(trailers)):
    clips.append(trailers[i])
    clips.append(splash())

final_clip = concatenate_videoclips(clips)
final_clip.write_videofile('./temp.mp4', fps=24)

final_clip = add_timer(VideoFileClip('temp.mp4').resize(height=1080))
final_clip.write_videofile('./final.mp4', fps=24)
