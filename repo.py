from utils import convertDesc, log, logr, format_filename, enablePrint, clearUTF8
from model import Video
import sys

# Lê roteiro.raw
def nmain(froteiro):
    roteiro = open(froteiro, "r", encoding="UTF-8")
    content = roteiro.readlines()
    lista = []

    logr(f"Carregando repositório .")

    for line in content:
        parse = line.split(" ")
        principal = parse[0]

        video = Video()
        video.root = principal

        video.link = parse[1]
        if (len(parse) == 2):
            lista.append(video)
            continue

        video.start = parse[2]
        video.end  = parse[3]
        video.descricao = clearUTF8("_".join(parse[4:(len(parse))]).replace("\r\n","").replace("\n","").replace("?","").replace(",","").replace(".",""))
        # video.descricao = convertDesc(parse[4:(len(parse))])
        # video.descricao = format_filename(parse[4:(len(parse))])
        lista.append(video)

    log(f"----------------------------------------------- Arquivos Base")

    for video in lista:
        if not video.rootExists():
            logr(f"o {video.root} - Iniciando download")
            video.download()
            log(f"v {video.root}")
        else:
            log(f"v {video.root}")
    
    log(f"---------------------------------------------------- Recortes")

    for video in lista:
        if not video.exists():
            logr(f"o {video.descricao} - Recorte não localizado.")
            video.process()
            log(f"v {video.descricao}")
        elif (video.descricao != None):
            log(f"v {video.descricao}")

if __name__ == "__main__":
    # step2(URL='https://www.youtube.com/watch?v=hbXljW9FnCc', filename="teste")
    nmain(sys.argv[1])
    log(f"---------------------------------------------------------- Fim")