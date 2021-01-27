import glob
import os
import shutil
import sys
import ffmpeg
from pathlib import Path
from pprint import pprint
from random import shuffle
from splash import gen_guide, gen_poster_array_with_text


# Required programs
def check_program(cmd):
    file = shutil.which(cmd)
    if str(file) == "None":
        sys.exit(cmd + " was not found on your system.")


check_program('ffprobe')
check_program('ffmpeg')


def check_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


check_dir('./output')
check_dir('./Posters')
check_dir('./Sessions')
check_dir('./Trailers')


def get_session_series(session):
    session_name = []
    for poster in glob.glob(glob.escape(session) + '/*'):
        p = Path(poster)
        name = p.stem
        session_name.append(name)
    return session_name


def gen_session_name(session, delimiter=" & "):
    return delimiter.join(get_session_series(session))


def gen_current_session_poster(session, duration=10):
    current_session_posters = [ffmpeg.input(poster, framerate=25, t=duration, loop=1)
                                   .filter('scale', 320, 450)
                               for poster in glob.glob(glob.escape(session) + '/*')]
    if len(current_session_posters) == 0:
        sys.exit("Please put posters in session folder '" + session + "'")
    if len(current_session_posters) > 1:
        session_frame = ffmpeg.filter(current_session_posters, 'hstack')
    else:
        session_frame = current_session_posters[0]
    return session_frame \
        .filter('pad', width=920, height=540, x='(ow-iw)/2', y='(oh-ih)', color='black') \
        .drawtext("This session:", fontsize=38, fontcolor='white', x='(w-tw)/2') \
        .drawtext(gen_session_name(session), fontsize=37, fontcolor='white', x='(w-tw)/2', y=48)


def get_trailers(session):
    series = get_session_series(session)
    return list(filter(lambda x: x not in series,
                       [{'input': ffmpeg.input(trailer), 'data': ffmpeg.probe(trailer)} for trailer in
                        glob.glob('Trailers/*.mp4')]))


# Durations are in seconds
def apply_fade(stream, total_duration, fade_duration):
    return stream.filter('fade', type='in', start_time=0, duration=fade_duration) \
        .filter('fade', type='out', start_time=total_duration - fade_duration, duration=fade_duration)


def gen_trailer_with_current_session(session, max_trailers=99):
    current_session_poster_duration = 10
    cs = apply_fade(gen_current_session_poster(session, current_session_poster_duration)
                    .filter('setsar', 1), current_session_poster_duration, 1).filter_multi_output('split')
    vids = []
    trailers = get_trailers(session)
    shuffle(trailers)
    nTrailers = len(trailers)
    if nTrailers > max_trailers:
        nTrailers = max_trailers
    for i in range(nTrailers):
        v = ffmpeg.concat(apply_fade(trailers[i]['input'].video.filter('scale', 920, 540).filter('setsar', 1),
                                     float(trailers[i]['data']['format']['duration']), 1), cs[i])
        a = trailers[i]['input'].audio
        vids += [v, a]
    return ffmpeg.concat(*vids, v=1, a=1)


def overlay_trailers(trailers_concat):
    return ffmpeg.filter([gen_poster_array_with_text(), ffmpeg.filter([gen_guide(), trailers_concat], 'vstack')],
                         'hstack')


def gen_countdown_file(length_in_sec, session):
    import datetime
    countdown = datetime.datetime.strptime('00:00:00', '%H:%M:%S') + datetime.timedelta(seconds=length_in_sec - 1)
    vtime_start = datetime.datetime.strptime('00:00:01', '%H:%M:%S')
    vtime_end = vtime_start + datetime.timedelta(seconds=1)
    subindex = 1
    timecheck = True
    f = open('output/' + session + ".ssa", "w")
    write = lambda s: f.write(s + '\n')
    while (timecheck):
        write(str(subindex))
        write(vtime_start.strftime('%H:%M:%S') + ",000 --> " + vtime_end.strftime('%H:%M:%S') + ",000")
        write("{\pos(350, 25}" + countdown.strftime('%#M:%S'))
        write("")
        timecheck = countdown.strftime('%M:%S') != '00:00'
        countdown = countdown - datetime.timedelta(seconds=1)
        vtime_start = vtime_start + datetime.timedelta(seconds=1)
        vtime_end = vtime_start + datetime.timedelta(seconds=1)
        subindex += 1
    f.close()


def render_session(session, max_trailers, codec, debug=False):
    session_name = session.split('/')[-1]
    out = overlay_trailers(gen_trailer_with_current_session(session, max_trailers)) \
        .output('output/' + session_name + '.mp4', vcodec=codec, pix_fmt="yuv420p").overwrite_output()
    if debug:
        f = open('output/' + session_name + '.graph.png', "wb")
        f.write(out.view(pipe=True))
        f.close()
        f = open('output/' + session_name + '-detailed.graph.png', "wb")
        f.write(out.view(pipe=True, detail=True))
        f.close()
        command = out.compile()
        pprint(command)
    else:
        out.run()
        gen_countdown_file(float(ffmpeg.probe('output/' + session_name + '.mp4')['format']['duration']),
                           session_name)


from PyInquirer import style_from_dict, Token, prompt

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

import argparse

parser = argparse.ArgumentParser(description='Render session pre-roll')
parser.add_argument('--h265', dest='h265_codec', action='store_const',
                    const="libx265", default="libx264",
                    help='Encode with h265')
parser.add_argument('--debug', dest='debug', action='store_true',
                    help='Debug ffmpeg command and filter nodes.')
parser.add_argument('--trailers', dest='max_trailers', metavar='N', type=int, nargs=1,
                    help='an integer for the accumulator')
args = parser.parse_args()

sessions = glob.glob('Sessions/*')
if len(sessions) == 0:
    sys.exit("Please add sessions in the Sessions directory.")
result = prompt({
    'type': 'checkbox',
    'name': 'sessions',
    'message': 'What session(s) do you want to render?',
    'choices': list(map(lambda s: {'name': s.split('/')[-1], 'value': s, 'checked': True}, sessions))
}, style=style)
if result:
    max_trailers = 99
    if args.max_trailers:
        max_trailers = args.max_trailers[0]
    for session in result['sessions']:
        render_session(session, max_trailers, args.h265_codec, args.debug)
