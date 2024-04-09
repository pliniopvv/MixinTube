from utils.prep import MyCut
from model import Video
import yt_dlp
import random
import shutil
import time
import os

# Lê roteiro.raw
def main():
    roteiro = open("roteiro.raw", "r", encoding="UTF-8")
    content = roteiro.readlines()
    for line in content:
        parse = line.split(" ")
        link = parse[0]
        init = parse[1]
        end  = parse[2]
        desc = "_".join(parse[3:(len(parse))])

        step2(link, desc)
        step3(desc, init, end)

def nmain():
    roteiro = open("roteiro.raw", "r", encoding="UTF-8")
    content = roteiro.readlines()
    lista = []

    for line in content:
        parse = line.split(" ")
        principal = parse[0]

        video = Video()
        video.root = principal
        video.link = parse[1]
        video.start = parse[2]
        video.end  = parse[3]
        video.descricao = "_".join(parse[4:(len(parse))]).replace("\r\n","").replace("\n","").replace("?","").replace(",","").replace(".","")
        lista.append(video)

    for video in lista:
        if not video.rootExists():
            video.download()
        
    for video in lista:
        if not video.exists():
            video.process()

# baixa vídeo do youtube
def step2(URL, filename="Nonamed"):
    # _URL = 'https://www.youtube.com/watch?v=hbXljW9FnCc'

    tmp_dir = f"tmp_{random.randrange(start=1000, stop=9999)}"
    exists = os.path.exists(tmp_dir)
    while exists:
        tmp_dir = f"tmp_{random.randrange(start=1000, stop=9999)}"
        exists = os.path.exists(tmp_dir)

    os.makedirs(tmp_dir)
    
    ydl_opts = {
        'paths': {'home': tmp_dir}
    }
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ydl.download(URL)
    step21(tmp_dir, filename)
    shutil.rmtree(tmp_dir)

# move arquivo salvo para diretório de vídeos comum e retorna o nome do arquivo;
def step21(tmp_dir='tmp_1773', filename="Nonamed"):
    arquivo = os.listdir(tmp_dir)[0]
    sarquivo = arquivo.split(".")
    sarquivo[0] = filename
    sarquivo = ".".join(sarquivo)

    src = os.path.abspath("/".join([tmp_dir, arquivo]))
    dest = os.path.abspath("/".join(['videos',sarquivo]))

    shutil.move(src, dest)
    return sarquivo

# realiza recorte
def step3(FILE, init, fim, desc):
    # _FILE = 'videos/Cardozo e Coppolla debatem se embate entre Moraes e Musk amplia polarização ｜ O GRANDE DEBATE [BwSrn07wkyI].webm'
    cut = MyCut(FILE, init, fim)
    cut.save(desc)

if __name__ == "__main__":
    # step2(URL='https://www.youtube.com/watch?v=hbXljW9FnCc', filename="teste")
    nmain()