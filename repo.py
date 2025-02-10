from utils import convertDesc, log, logr, format_filename, enablePrint, clearUTF8
from model import Video
from core import parse_roteiro, download_all_videos, cut_all_videos
import sys

# Lê roteiro.raw
def nmain(froteiro):
    lista = parse_roteiro(froteiro)

    log(f"----------------------------------------------- Arquivos Base")

    download_all_videos(lista)
    
    log(f"---------------------------------------------------- Recortes")

    cut_all_videos(lista)

if __name__ == "__main__":
    nmain(sys.argv[1])
    log(f"---------------------------------------------------------- Fim")