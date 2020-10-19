from moviepy.editor import *


def add_timer(clip):
    def get_time_array(i):
        minutes = ''
        sec = str(i % 60)
        if int(i / 60) > 0:
            minutes = str(int(i / 60)) + ':'
            if i % 60 < 10:
                sec = '0' + sec
        return TextClip(minutes + sec, color='white', fontsize=50).subclip(0, 1)

    timer_clip = concatenate_videoclips([get_time_array(i) for i in range(int(clip.end), 0, -1)])

    return CompositeVideoClip([
        clip,
        timer_clip.set_position((clip.size[0] - timer_clip.size[0], clip.size[1] - timer_clip.size[1]))
    ], size=clip.size)


if __name__ == "__main__":
    from time import time

    clip = VideoFileClip('Trailers/Strike Witches.mp4').resize(height=1080)
    t = time()
    final_clip = add_timer(clip).subclip(0, 5)
    print(time() - t)
    final_clip.write_videofile('./output.mp4', fps=24)
