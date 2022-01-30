import eel
import os
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
        yt.streams.filter(file_extension='mp4').first().download()
        file_name = [x for x in os.listdir('.') if name in x and '.mp4' in x][0]
        video = VideoFileClip(file_name)
        video.audio.write_audiofile(file_name.replace('.mp4','.mp3'))
        video.close()
        if before_exist:
            os.rename(file_name_,file_name_.replace('.await','.mp4'))
            return
        else:
            os.remove(file_name)
    if option == '360p':
        yt.streams.filter(res="360p",file_extension='mp4').first().download()
    if option == '720p':
        yt.streams.filter(res="720p",file_extension='mp4').first().download()


eel.start('index.html', size=(400,150))