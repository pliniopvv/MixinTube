from utils import convertDesc
from model import Video
import sys

# Lê roteiro.raw
def nmain(froteiro):
    roteiro = open(froteiro, "r", encoding="UTF-8")
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
        # video.descricao = convertDesc(parse[4:(len(parse))])
        lista.append(video)

    for video in lista:
        if not video.rootExists():
            video.download()
        
    for video in lista:
        if not video.exists():
            video.process()

if __name__ == "__main__":
    # step2(URL='https://www.youtube.com/watch?v=hbXljW9FnCc', filename="teste")
    nmain(sys.argv[1])