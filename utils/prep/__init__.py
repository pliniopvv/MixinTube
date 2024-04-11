from moviepy.editor import *
from utils import enablePrint

class MyCut:
    def __init__(self, arquivo, inicio, fim):
        video = VideoFileClip(f"{arquivo}").subclip(inicio, fim)
        self.result = CompositeVideoClip([video])

    def save(self, arquivo="recorte"):
        from model import Config
        self.result.write_videofile(f"{Config.OUTPUT}/{arquivo}.webm")
