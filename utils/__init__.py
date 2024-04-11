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

def log(msg):
    print(msg)