import glob
import math
import re

from moviepy.editor import *
from splash import splash
from timer import add_timer
import os

between_splash = False
update = False

for arg in sys.argv[1:]:
    if arg == '-big' or arg == '-bigTrailers':
        between_splash = True
    elif arg == '-force':
        update = True


if not os.path.isdir('output'):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(ROOT_DIR, "output")
    os.mkdir(path)

if update or not os.path.isfile('output/stage1 splash.mp4'):
    splash().write_videofile('output/stage1 splash.mp4', fps=24)
    update = True

if update or not os.path.isfile('output/stage2 trailers.mp4'):
    def parse_trailer(t):
        clip = VideoFileClip(t)
        start = re.findall("trim_start=(\d*)", t)
        end = re.findall("trim_end=(\d*)", t)
        if end:
            clip = clip.subclip(t_end=clip.end - int(end[0]))
        if start:
            clip = clip.subclip(t_start=int(start[0]))
        return clip.volumex(0.4).resize(width=1920).fadein(1).fadeout(1)

    current_session_poster = glob.glob('Session/*')
    if len(current_session_poster) > 0:
        poster = ImageClip(current_session_poster[0])
        title = TextClip(current_session_poster[0].split('.')[0], color='white', fontsize=40)
        current_session = CompositeVideoClip([
            title,
            poster.resize(height=540 - title.size[1] + 10).set_position((0, title.size[1] + 10))
        ], size=(920, 540)).to_ImageClip().subclip(0, 10)

    trailers = [parse_trailer(t) for t in glob.glob('Trailers/*.mp4')]
    splash_clip = VideoFileClip('output/stage1 splash.mp4')

    if between_splash:
        if current_session:
            splash_clip = CompositeVideoClip([
                splash_clip,
                current_session.subclip(0, splash_clip.end).resize(width=900).set_position(('right', 'bottom'))
            ])
        splash_clip = splash_clip.fadein(1).fadeout(1)
        clips = [splash_clip]
        for i in range(0, len(trailers)):
            clips.append(trailers[i])
            clips.append(splash_clip)
        final_clip = concatenate_videoclips(clips)
    else:
        if current_session:
            trailers_with_session = []
            for i in range(len(trailers)):
                trailers_with_session.append(trailers[i])
                trailers_with_session.append(current_session.fadein(1).fadeout(1))
            trailers_clip = concatenate_videoclips(trailers_with_session)
            splash_clip = splash_clip.loop(math.ceil(trailers_clip.end / splash_clip.end))
            trailers_clip = concatenate_videoclips(
                [trailers_clip,
                 current_session.loop(math.ceil((splash_clip.end - trailers_clip.end) / current_session.end))
                     .subclip(0, splash_clip.end - trailers_clip.end).fadein(1)
                 ])
        else:
            trailers_clip = concatenate_videoclips(trailers)
            splash_clip = splash_clip.loop(math.ceil(trailers_clip.end / splash_clip.end))
        final_clip = CompositeVideoClip(
            [splash_clip, trailers_clip.resize(width=900).set_position(('right', 'bottom'))])

    final_clip.write_videofile('output/stage2 trailers.mp4', fps=24)
    update = True

if update or not os.path.isfile('output/final.mp4'):
    final_clip = add_timer(VideoFileClip('output/stage2 trailers.mp4')).fadeout(2)
    final_clip.write_videofile('output/final.mp4', fps=24)
