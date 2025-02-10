from utils import convertDesc, log, logr
from model import Video

def parse_roteiro(froteiro):
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

        if len(parse) == 2:
            continue

        video.start = parse[2]
        video.end  = parse[3]
        video.descricao = "_".join(parse[4:(len(parse))]).replace("\r\n","").replace("\n","").replace("?","").replace(",","").replace(".","")
        # video.descricao = convertDesc(parse[4:(len(parse))])
        lista.append(video)
    
    return lista

def download_all_videos(lista):
    for video in lista:
        if not video.rootExists():
            logr(f"o {video.root} - Iniciando download")
            video.download()
            log(f"v {video.root}")
        else:
            log(f"v {video.root}")

def cut_all_videos(lista):
    for video in lista:
        if not video.exists():
            logr(f"o {video.descricao} - Recorte não localizado.")
            video.process()
            log(f"v {video.descricao}")
        else:
            log(f"v {video.descricao}")

def group_by(lista):
    ordened = {}
    for video in lista:
        if video.root not in ordened:
            ordened[video.root] = []
        ordened[video.root].append(video)
    return ordened