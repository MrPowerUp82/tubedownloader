import yt_dlp, eel, os, sys, shutil
import imageio_ffmpeg

eel.init('web')

if sys.argv[0].endswith('.py'):
    # Encontra o caminho para a pasta site-packages, onde as bibliotecas Python estão instaladas
    site_packages_dir = next(p for p in sys.path if 'site-packages' in p)

    # Caminho para a pasta binaries do pacote 'imageio_ffmpeg'
    path_exe = os.path.join(site_packages_dir, 'imageio_ffmpeg', 'binaries')
else:
    path_exe = os.path.abspath(os.path.join(os.path.join(eel.root_path, '..'), 'imageio_ffmpeg', 'binaries'))

# Verifica se o diretório binaries existe
if not os.path.isdir(path_exe):
    raise FileNotFoundError(f"Diretório 'binaries' não encontrado em {path_exe}")

print(f"Localizando ffmpeg em: {path_exe}")

# Localiza o executável ffmpeg dentro do diretório binaries
ffmpeg_exe = next((x for x in os.listdir(path_exe) if 'ffmpeg' in x and x.endswith('.exe')), None)
if not ffmpeg_exe:
    raise FileNotFoundError("Executável ffmpeg não encontrado no diretório de 'binaries'.")

# Caminho completo para o executável do ffmpeg
filename_exe = os.path.join(path_exe, ffmpeg_exe)
if sys.argv[0].endswith('.py'):
    shutil.copyfile(filename_exe, os.path.join(os.path.dirname(__file__), 'ffmpeg.exe'))
else:
    shutil.move(filename_exe, os.path.join(path_exe, 'ffmpeg.exe'))
    os.environ["PATH"] += os.pathsep + path_exe
    
# Define variáveis de ambiente para o ffmpeg
os.environ["FFMPEG_BINARY"] = filename_exe
os.environ["IMAGEIO_FFMPEG_EXE"] = filename_exe

print(f"FFmpeg configurado em: {filename_exe}")


@eel.expose
def get_info(url):
    # Extrai as informações do vídeo sem baixá-lo
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        if info.get('thumbnail', False):
            return [info['title'], info['thumbnail']]
        else:
            return [info['title'], info['thumbnails'][0]['url']]

@eel.expose
def download(url, option):
    # Define opções de download baseadas na seleção do usuário
    ydl_opts = {}

    if option == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
        })
    elif option == 'playlist':
        ydl_opts = {'format': 'bestvideo+bestaudio/best', 'outtmpl': 'playlist/%(title)s.%(ext)s'}
    elif option == '360p':
        ydl_opts = {'format': 'bestvideo[height<=360]+bestaudio/best', 'outtmpl': '%(title)s.%(ext)s'}
    elif option == '720p':
        ydl_opts = {'format': 'bestvideo[height<=720]+bestaudio/best', 'outtmpl': '%(title)s.%(ext)s'}
    elif option == '1080p':
        ydl_opts = {'format': 'bestvideo[height<=1080]+bestaudio/best', 'outtmpl': '%(title)s.%(ext)s'}

    # Faz o download com as opções definidas
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Inicia a interface do Eel
eel.start('index.html', size=(400, 150))
