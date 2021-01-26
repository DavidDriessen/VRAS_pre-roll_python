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


def gen_current_session_poster(session):
    current_session_posters = [ffmpeg.input(poster, framerate=25, t=5, loop=1)
                                   .filter('scale', 320, 450, force_original_aspect_ratio='decrease')
                                   .filter('pad', width=320, height=450, x='(ow-iw)/2', y='(oh-ih)/2', color='black')
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
                       [ffmpeg.input(trailer) for trailer in glob.glob('Trailers/*.mp4')]))


def gen_trailer_with_current_session(session):
    cs = gen_current_session_poster(session).filter('setsar', 1).filter_multi_output('split')
    vids = []
    trailers = get_trailers(session)
    shuffle(trailers)
    for i in range(len(trailers)):
        v = ffmpeg.concat(trailers[i].video.filter('scale', 920, 540).filter('setsar', 1), cs[i])
        a = trailers[i].audio
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


def render_session(session, debug=False):
    session_name = session.split('/')[-1]
    out = overlay_trailers(gen_trailer_with_current_session(session)) \
        .output('output/' + session_name + '.mp4').overwrite_output()
    if debug:
        out.view()
        command = out.compile()
        pprint(command)
        print()
        print(' '.join(command).replace('-filter_complex ', '-filter_complex \'').replace(' -map', '\' -map'))
    else:
        out.run()
        gen_countdown_file(float(ffmpeg.probe('output/' + session_name + '.mp4')['format']['duration']),
                           session_name)


def render_all_sessions(debug=False):
    sessions = glob.glob('Sessions/*')
    if len(sessions) == 0:
        sys.exit("Please add sessions in the Sessions directory.")
    for session in sessions:
        render_session(session, debug)


render_all_sessions()
