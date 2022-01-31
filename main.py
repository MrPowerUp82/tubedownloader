# set ffmpeg bin.
import os
import sys
if 'main.py' in sys.argv[0]:
    print('dev mode')
else:
    print('build mode')
    path_exe = os.path.expanduser('~')+'\\AppData\Local\\Temp\\tubedownloader\\'
    path_exe = path_exe+os.listdir(path_exe)[0]+'\\imageio_ffmpeg\\binaries\\'
    path_exe = path_exe + [x for x in os.listdir(path_exe) if 'ffmpeg' in x and '.exe' in x][0]
    os.environ["FFMPEG_BINARY"] = path_exe
    os.environ["IMAGEIO_FFMPEG_EXE"] = path_exe
    # resolve to build
    from moviepy.audio.fx.audio_fadein import audio_fadein
    from moviepy.audio.fx.audio_fadeout import audio_fadeout
    from moviepy.audio.fx.audio_normalize import audio_normalize
    from moviepy.audio.fx.audio_loop import audio_loop

    # resolve to build
    from moviepy.video.fx.accel_decel import accel_decel
    from moviepy.video.fx.blackwhite import blackwhite
    from moviepy.video.fx.blink import blink
    from moviepy.video.fx.crop import crop
    from moviepy.video.fx.even_size import even_size
    from moviepy.video.fx.fadein import fadein
    from moviepy.video.fx.fadeout import fadeout
    from moviepy.video.fx.mirror_x import mirror_x
    from moviepy.video.fx.mirror_y import mirror_y
    from moviepy.video.fx.resize import resize
    from moviepy.video.fx.invert_colors import invert_colors
    from moviepy.video.fx.loop import loop
    from moviepy.video.fx.margin import margin
    from moviepy.video.fx.mask_and import mask_and
    from moviepy.video.fx.mask_or import mask_or
    from moviepy.video.fx.mirror_x import mirror_x
    from moviepy.video.fx.mirror_y import mirror_y
    from moviepy.video.fx.rotate import rotate
    from moviepy.video.fx.speedx import speedx

    # resolve to build
    import imageio_ffmpeg

# lib's principais
import eel
from moviepy.editor import VideoFileClip
from pytube import YouTube


eel.init('web')


@eel.expose
def get_info(url):
    yt=YouTube(url)
    return [yt.title,yt.thumbnail_url]

@eel.expose
def download(url,option):
    yt=YouTube(url)
    if option == 'mp3':
        name = yt.title
        before_exist = [True for x in os.listdir('.') if name in x]
        if before_exist:
            file_name_ = [x for x in os.listdir('.') if name in x][0]
            os.rename(file_name_,file_name_.replace('.mp4','.await'))
            file_name_ = file_name_.replace('.mp4','.await')
        yt.streams.filter(file_extension='mp4',progressive=True).first().download()
        file_name = [x for x in os.listdir('.') if name in x and '.mp4' in x][0]
        video = VideoFileClip(file_name)
        video.audio.write_audiofile(file_name.replace('.mp4','.mp3'))
        video.close()
        if before_exist:
            os.remove(file_name)
            os.rename(file_name_,file_name_.replace('.await','.mp4'))
            return
        else:
            os.remove(file_name)
    if option == '360p':
        video_stream = yt.streams.filter(res="360p",file_extension='mp4',progressive=True)
        if len(video_stream) < 1:
            video_stream = yt.streams.filter(res="240p",file_extension='mp4',progressive=True)
        video_stream.first().download()
    if option == '720p':
        video_stream = yt.streams.filter(res="1080p",file_extension='mp4',progressive=True)
        if len(video_stream) < 1:
            video_stream = yt.streams.filter(res="720p",file_extension='mp4',progressive=True)
        video_stream.first().download()


eel.start('index.html', size=(400,150))