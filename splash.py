from math import ceil

from moviepy.editor import *
import glob
from random import shuffle

font = "./font.ttf"
guideText = ["If your microphone picks up some background noise(hiss, cars,\n"
             "family members). Please mute your microphone and unmute when\n"
             "you want to say something. If you are on oculus quest, use\n"
             "push-to-talk. If you are on rift S, use different microphone than\n"
             "the headset. This is because the rift S microphone will start\n"
             "turning your voice into a robot.",
             "Please refrain from using drawing tools in BigScreen. This is\n"
             "because drawings are very obstructive"
             ]


def text_block(title, text, width=960):
    title_clip = TextClip(title, color='white', font=font, fontsize=40, align='West')
    text_clip = TextClip(text, color='white', font=font, fontsize=25, align='West')
    return CompositeVideoClip([title_clip, text_clip.set_position((0, title_clip.size[1] + 5))],
                              size=(width, title_clip.size[1] + text_clip.size[1] + 5))


def right(width=960):
    title = TextClip("Guidelines", color='white', font=font, fontsize=55, align='West')
    audio = text_block("Audio:", guideText[0], width).set_position((20, title.size[1] + 10))
    toys = text_block("Toys / other items:", guideText[1], width).set_position(
        (20, title.size[1] + 10 + audio.size[1] + 10))
    return CompositeVideoClip([title, audio, toys], size=(width, int(1080))).to_ImageClip()


def left(width=960, length=20):
    # title = TextClip("Currently showing the following and more", color='white', fontsize=50, align='West')
    title = TextClip("Sign up at: www.vranimesociety.com\nCurrently showing the following shows", color='white',
                     font=font, fontsize=50, align='West')
    poster_glob = glob.glob("Posters/*")
    if len(poster_glob) < 6:
        sys.exit("There are not enough posters in the Posters folder. Please add atleast 6 posters.")
    shuffle(poster_glob)
    posters_arr = []
    for i in range(0, 6):
        posters_arr.append(poster_glob[i])
    posters = []
    for p in posters_arr:
        try:
            posters.append(ImageClip(p).resize((width / 3, 450)))
        except ValueError:
            sys.exit("{0} is incompatible with moviepy. Please use a different poster".format(p))
    if len(posters) % 2:
        posters.append(ColorClip((width / 3, 450), (0, 0, 0)))
    half = len(posters) // 2
    if len(posters) > 6:
        posters_array = clips_array([posters[half:] + posters[half:], posters[:half] + posters[:half]])
        return CompositeVideoClip([
            title.set_position((0, 30)),
            posters_array.set_position(
                lambda t: (-(int((t * (width / 3 / (length / half)))) % (width / 3 * half)), 'bottom'))
        ], size=(width, int(1080)))
    posters_array = clips_array([posters[half:], posters[:half]])
    return CompositeVideoClip([title.set_position((0, 30)), posters_array.set_position((0, 'bottom'))],
                              size=(width, int(1080)))


def splash():
    return clips_array([[left().margin(right=40), right(920)]]).subclip(0, 20)


if __name__ == '__main__':
    splash().write_videofile('output/stage1 splash.mp4', fps=24)
