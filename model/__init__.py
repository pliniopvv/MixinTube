from utils.prep import MyCut
from moviepy.editor import *
from PIL import Image
import yt_dlp
import random
import shutil
import math
import os

class Video:
    def __init__(self):
        self.rootfile = None
        self.file = None
        pass

    def rootExists(self):
        if os.path.exists(os.path.abspath(f"{Config.OUTPUT}/{self.root}.webm")):
            return True
        else:
            return self.rootfile != None
    
    def exists(self):
        if os.path.exists(os.path.abspath(f"{Config.OUTPUT}/{self.descricao}.webm")):
            return True
        return self.file != None
    
    def download(self):
        tmp_dir = f"tmp_{random.randrange(start=1000, stop=9999)}"
        exists = os.path.exists(tmp_dir)

        while exists:
            tmp_dir = f"tmp_{random.randrange(start=1000, stop=9999)}"
            exists = os.path.exists(tmp_dir)
        os.makedirs(tmp_dir)
        
        ydl_opts = {
            'paths': {'home': tmp_dir}
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.download(self.link)

        arquivo = os.listdir(tmp_dir)[0]
        sarquivo = arquivo.split(".")
        sarquivo[0] = self.root
        sarquivo = ".".join(sarquivo)

        src = os.path.abspath("/".join([tmp_dir, arquivo]))
        dest = os.path.abspath("/".join([Config.OUTPUT, sarquivo]))

        shutil.move(src, dest)
        shutil.rmtree(tmp_dir)
        
        self.rootfile = sarquivo
        return sarquivo
    
    def process(self):
        if (self.rootfile == None): self.rootfile = f"{self.root}.webm"
        file = os.path.abspath("/".join([Config.OUTPUT, f"{self.root}.webm"]))
        cut = MyCut(file, self.start, self.end)
        cut.save(self.descricao)













class Cut:
    def __init__(self, parametros):
        arquivos = []
        key = -1
        for item in parametros:
            key += 1
            if key == 0:
                self.output = item
            else:
                arquivo = f"{item}.webm"
                if not os.path.exists(os.path.abspath(f"{Config.OUTPUT}/{arquivo}")):
                    raise FileNotFoundError(f"Arquivo {arquivo} não encontrado em /{Config.OUTPUT}/!")
                arquivos.append(arquivo)
        self.arquivos = arquivos

    def compile(self):
        videos = []

        for arquivo in self.arquivos:
            video = VideoFileClip(f"{Config.OUTPUT}/{arquivo}")
            videos.append(video)

        result = concatenate_videoclips(videos)
        result.write_videofile(f"{Config.OUTPUT}/{self.output}.webm")







class MontagemBuilder:
    def __init__(self):
        self.cmd = None
        self.montagem = None
        self.scope = None

    def state(self, cmd):
        stream = cmd.split(" ")
        self.cmd = stream[0]
        self.output = None
        if len(stream) > 1:
            self.output = stream[1]
        pass

    def openScope(self):
        child = None
        if self.cmd == 'concat':
            child = MontagemConcat()
        elif self.cmd == 'array':
            child = MontagemArray()

        if self.montagem == None:
            self.montagem = child
            self.scope = child
        else:
            scope = self.montagem.scope()
            if scope == self.montagem:
                self.montagem.child = child
                scope = child
            else:
                self.scope = scope

    def closeScope(self):
        self.montagem = None
        pass
    def injectVideo(self, filename):
        if self.cmd == 'concat':
            video = VideoFileClip(f"{Config.OUTPUT}/{filename}.webm")
            self.scope.add(video)
        elif self.cmd == 'array':
            video = VideoFileClip(f"{Config.OUTPUT}/{filename}.webm")
            self.scope.add(video)
        pass
    def compile(self):
        self.scope.compile(self.output)
    def hasScopeOpened(self):
        return self.montagem != None

class Montagem:
    def __init__(self):
        self.repo = []
        self.child = None
    def openScope(self):
        self.child = []
    def closeScope(self):
        self.child = None
    def hasChild(self):
        return self.child != None
    def scope(self):
        if self.child == None:
            return self
        else:
            return self.child.scope()
    def add(self, video):
        self.repo.append(video)

class MontagemConcat(Montagem):
    def __init__(self):
        super().__init__()
        self.child = None
        pass
    def compile(self, output):

        width = 0
        for video in self.repo:
            if width > video.size[0]:
                width = video.size[0]

        for video in self.repo:
            video.resize(width=width)

        result = concatenate_videoclips(self.repo)
        result.write_videofile(f"{Config.OUTPUT}/{output}.webm")



class MontagemArray(Montagem):
    def __init__(self):
        super().__init__()
        pass
    def compile(self, output):
        lado = math.floor(math.sqrt(len(self.repo)))
        repo = []
        for x in range(lado):
            inner = []
            for y in range(lado):
                inner.append(self.repo[(x*2)+(x+y)])
            repo.append(inner)

        mWidth = 0
        mHeight = 0

        for x in range(lado):
            for y in range(lado):
                width = repo[x][y].size[0]
                height = repo[x][y].size[1]
                if width > mWidth:
                    mWidth = width
                if height > mHeight:
                    mHeight = height
                
        for x in range(lado):
            for y in range(lado):
                repo[x][y] = repo[x][y].resize(width=mWidth)
                print(f"### FRAME {x},{y}: {repo[x][y].filename}")

        result = clips_array(repo)
        result.write_videofile(f"{Config.OUTPUT}/{output}.webm")












class Config:
    OUTPUT = 'videos'