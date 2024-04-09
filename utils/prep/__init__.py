from moviepy.editor import *
    
class MyCut:
    def __init__(self, arquivo, inicio, fim):
        video = VideoFileClip(f"{arquivo}.webm").subclip(inicio, fim)
        self.result = CompositeVideoClip([video])

    def save(self, arquivo="recorte"):
        self.result.write_videofile(f"{arquivo}.webm")
