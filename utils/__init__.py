import sys, os

def convertDesc(desc):
    return "_".join(desc.split(" ")).replace("\r\n","").replace("\n","").replace("?","").replace(",","").replace(".","")

def format_filename(linha):
    return convertDesc(linha)

def clearUTF8(linha):
    return (
        linha
        .replace("\t","")
        .replace("\r\n","")
        # .replace("\n","")
        .replace("?","")
        .replace(",","")
        .replace(".","")
        .strip()
        )

def blockPrint():
    sys.stdout = open(os.devnull, "w")

def enablePrint():
    sys.stdout = sys.__stdout__

def log(msg):
    enablePrint()
    print(msg)
    blockPrint()

def logr(msg):
    enablePrint()
    print(msg, end="\r")
    blockPrint()
