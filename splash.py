from math import ceil

from moviepy.editor import *
import glob
from random import shuffle

guideText = ["If your microphone picks up some background noise\n"
             "(hiss, cars, family members). Please mute your microphone\n"
             "and unmute when you want to say something.\n"
             "If you are on oculus quest, use push-to-talk.\n"
             "If you are on rift S, use different microphone than\n"
             "the headset. This is because the rift S microphone\n"
             "will start turning your voice into a robot.",
             "Please refrain from using drawing tools in BigScreen.\n"
             "This is because drawings are very obstructive\n"
             "and you might not be able to rid of them.\n"
             "You can use the other ones(tomatoes, popcorn)\n"
             "as long you don't spam them."
             ]


def text_block(title, text, width=960):
    title_clip = TextClip(title, color='white', fontsize=40, align='West')
    text_clip = TextClip(text, color='white', fontsize=25, align='West')
    return CompositeVideoClip([title_clip, text_clip.set_position((0, title_clip.size[1] + 5))],
                              size=(width, title_clip.size[1] + text_clip.size[1] + 5))


def right(width=960):
    title = TextClip("Guidelines", color='white', fontsize=55, align='West')
    audio = text_block("Audio:", guideText[0], width).set_position((20, title.size[1] + 10))
    toys = text_block("Toys / other items:", guideText[1], width).set_position(
        (20, title.size[1] + 10 + audio.size[1] + 10))
    return CompositeVideoClip([title, audio, toys], size=(width, int(1080))).to_ImageClip()


def left(width=960, length=20):
    # title = TextClip("Currently showing the following and more", color='white', fontsize=50, align='West')
    title = TextClip("Sign up at: www.vranimesociety.com\nCurrently showing the following shows", color='white',
                     fontsize=52, align='West')
    poster_glob = glob.glob("Posters/*")
    if len(poster_glob) < 6:
        sys.exit("There are not enough posters in the Posters folder. Please add atleast 6 posters.")
        pass
    shuffle(poster_glob)
    posters_arr = []
    for i in range(0,6):
        posters_arr.append( poster_glob[i] )
        pass
    posters = [ImageClip(p).resize((width / 3, 450)) for p in posters_arr]
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
