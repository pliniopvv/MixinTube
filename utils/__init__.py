
def convertDesc(desc):
    return "_".join(desc.split(" ")).replace("\r\n","").replace("\n","").replace("?","").replace(",","").replace(".","")