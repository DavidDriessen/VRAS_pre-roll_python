from moviepy.editor import *
import glob

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
    title_clip = TextClip(title, color='white', fontsize=55, align='West')
    text_clip = TextClip(text, color='white', fontsize=35, align='West')
    return CompositeVideoClip([title_clip, text_clip.set_position((0, title_clip.size[1] + 10))],
                              size=(width, title_clip.size[1] + text_clip.size[1] + 10))


def right(width=960):
    title = TextClip("Guidelines", color='white', fontsize=60, align='West')
    audio = text_block("Audio:", guideText[0], width).set_position((20, title.size[1] + 10))
    toys = text_block("Toys / other items:", guideText[1], width).set_position((20, title.size[1] + 10 + audio.size[1] + 10))
    return CompositeVideoClip([title, audio, toys], size=(width, int(1080))).to_ImageClip()


def left(width=960):
    title = TextClip("Currently showing the following and more", color='white', fontsize=50, align='West')
    posters = [ImageClip(p).resize((320, 500)) for p in glob.glob('Posters/*.jpg')]
    posters_array = clips_array([[posters[0], posters[1], posters[2]], [posters[3], posters[4], posters[5]]])
    return CompositeVideoClip([title, posters_array.set_pos((0, title.size[1] + 10))],
                              size=(width, int(1080))).to_ImageClip()


def splash():
    return clips_array([[left(1000), right(920)]]).subclip(0, 30).fadein(1).fadeout(1)


if __name__ == '__main__':
    splash().write_videofile('./output.mp4', fps=1)
