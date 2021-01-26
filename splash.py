from random import shuffle
import ffmpeg
import glob

import sys

font = "./font.ttf"
guideText = [{'title': "Audio:",
              'text': [
                  "If your microphone picks up some background noise(hiss, cars,",
                  "family members). Please mute your microphone and unmute when",
                  "you want to say something. If you are on oculus quest, use",
                  "push-to-talk. If you are on rift S, use different microphone than",
                  "the headset. This is because the rift S microphone will start",
                  "turning your voice into a robot."]},
             {'title': "Toys / other items:",
              'text': [
                  "Please refrain from using drawing tools in BigScreen. This is",
                  "because drawings are very obstructive"]}
             ]


def gen_guide():
    res = ffmpeg.input("color=size=920x540:duration=10:rate=25:color=black", f='lavfi') \
        .drawtext("Guidelines", fontsize=55, fontcolor='white', y=40)
    offset = 55 + 10 + 40  # Size of header plus spacing below plus spacing above
    for text in guideText:
        res = res.drawtext(text['title'], fontsize=40, fontcolor='white', x=10, y=offset)
        offset += 40 + 10  # Size of title plus spacing below
        res = res.drawtext('\n'.join(text['text']), fontsize=25, fontcolor='white', x=20, y=offset, line_spacing=10)
        offset += (25 + 10) * len(text['text']) + 10  # (Size of text plus line_spacing) times rows plus spacing below
    return res


def gen_poster_array():
    poster_glob = glob.glob("Posters/*")
    if len(poster_glob) < 6:
        sys.exit("There are not enough posters in the Posters folder. Please add atleast 6 posters.")
    shuffle(poster_glob)
    posters = []
    for i in range(0, 6):
        posters.append(
            ffmpeg.input(poster_glob[i])
                .filter('scale', 990 / 3, 460))
    row1 = ffmpeg.filter(posters[:3], 'hstack', inputs=len(posters[:3]))
    row2 = ffmpeg.filter(posters[3:], 'hstack', inputs=len(posters[3:]))
    return ffmpeg.filter([row1, row2], 'vstack')


def gen_poster_array_with_text():
    return gen_poster_array() \
        .filter('pad', width=1000, height=1080, x=0, y='(oh-ih)', color='black') \
        .drawtext("Sign up at: www.vranimesociety.com\nCurrently showing the following shows",
                  fontcolor='white', fontsize=50, x=10, y=40)
