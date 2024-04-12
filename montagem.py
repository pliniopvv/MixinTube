from model import Montagem, MontagemBuilder
from utils import clearUTF8, format_filename, log, logr
import sys
import os

builder = MontagemBuilder()

def main(froteiro):
    global builder
    stream = open(froteiro, "r", encoding="UTF-8")
    linhas = stream.readlines()
    log(f"#### {froteiro} ####")
    log(f"")
    for linha in linhas:
        clinha = clearUTF8(linha)
        if isCmd(clinha):
            setCmd(clinha)
        elif isOpenScope(clinha):
            builder.openScope()
        elif isCloseScope(clinha):
            builder.closeScope()
            if not builder.hasScopeOpened():
                builder.compile()
                builder = MontagemBuilder()
        else:
            addScoped(format_filename(clinha))

def isCmd(linha):
    stream = linha.split(" ")
    return stream[0] in ['concat', 'array', 'midnight']

def setCmd(linha):
    builder.state(linha)

def isScope(linha):
    return linha in ['[',']']

def isOpenScope(linha):
    return linha == '['

def isCloseScope(linha):
    return linha == ']'

def toggleScope(linha):
    if linha == '[':
        log(f"------------------------- Adicionando arquivos")
        builder.openScope()
    elif linha == ']':
        builder.closeScope()
    else:
        raise IndexError("Comando equivocado para o escopo!")
    
def addScoped(linha):
    # print(f"#### {builder.cmd} vídeo injetado: {linha}")
    builder.injectVideo(linha)



if __name__ == '__main__':
    main(sys.argv[1])