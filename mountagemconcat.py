from utils import convertDesc
from model import Cut
import sys
import os


def main():
    arquivo = os.path.abspath(sys.argv[1])
    stream = open(arquivo, "r", encoding="UTF-8")
    linhas = stream.readlines()
    for linha in linhas:
        parametros = convertDesc(linha).split("|")
        cut = Cut(parametros)
        cut.compile()

if __name__ == '__main__':
    main()