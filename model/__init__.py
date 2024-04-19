from utils import log, logr, enablePrint
from utils.prep import MyCut
from moviepy.editor import *
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
        logr(f"o {self.root} - Criando pasta temporária")
        tmp_dir = f"tmp_{random.randrange(start=1000, stop=9999)}"
        exists = os.path.exists(tmp_dir)

        while exists:
            tmp_dir = f"tmp_{random.randrange(start=1000, stop=9999)}"
            exists = os.path.exists(tmp_dir)
        os.makedirs(tmp_dir)
        
        
        ydl_opts = {
            'paths': {'home': tmp_dir},
            # 'format': 'webm',
            'quiet': True,
            'consoletitle': True,
            # 'format': 'vext'
        }
        logr(f"o {self.root} - Baixando vídeo              ")
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.download(self.link)

        logr(f"o {self.root} - Organizando")
        arquivo = os.listdir(tmp_dir)[0]
        sarquivo = arquivo.split(".")
        ext = sarquivo[len(sarquivo)-1]
        sarquivo = []
        sarquivo.append(self.root)
        sarquivo.append(ext)
        sarquivo = ".".join(sarquivo)

        src = os.path.abspath("/".join([tmp_dir, arquivo]))
        dest = os.path.abspath("/".join([Config.OUTPUT, sarquivo]))

        shutil.move(src, dest)
        shutil.rmtree(tmp_dir)
        
        self.rootfile = sarquivo
        return sarquivo
    
    def process(self):
        logr(f"o {self.descricao} - Recortando.")
        if (self.rootfile == None): self.rootfile = f"{self.root}.webm"
        file = os.path.abspath("/".join([Config.OUTPUT, f"{self.root}.webm"]))
        if (self.start == self.end): return None
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
        log(f"------------------------- Exec {stream[0]}")
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
        elif self.cmd == 'midnight':
            child = MontagemMidnight()

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
        arquivo = f"{Config.OUTPUT}/{filename}.webm"
        _video = VideoFileClip(arquivo)
        if not os.path.exists(os.path.abspath(arquivo)):
            log(f"x {filename}.webm - Arquivo não localizado!")
        else:
            log(f"v {filename}.webm")
        if self.cmd == 'concat':
            self.scope.add(_video)
        elif self.cmd == 'array':
            self.scope.add(_video)
        elif self.cmd == 'midnight':
            self.scope.add(_video)
        pass
    def compile(self):
        aOutput = f"{Config.OUTPUT}/{self.output}.webm"
        log(f"------------------------- Operação de montagem")
        if not os.path.exists(os.path.abspath(aOutput)):
            logr(f"o {self.output}.webm - Iniciando montagem")
            self.scope.compile(aOutput)
            log(f"v {self.output}.webm - Montado")
        else:
            log(f"v {self.output}.webm - já disponível no repositório!")
            self.scope.close()
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
    def close(self):
        for video in self.repo:
            video.close()
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
        height = 0
        for video in self.repo:
            if video.size[0] > width:
                width = video.size[0]
            if video.size[1] > height:
                height = video.size[1]

        repo = []
        for video in self.repo:
            repo.append(video.resize((width, height)))

        result = concatenate_videoclips(repo)
        result.write_videofile(output)

# env\Scripts\activate && python montagem.py raw\montagem\montagem.raw
# cls && python montagem.py raw\montagem\montagem.raw

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
                repo[x][y] = repo[x][y].resize((mWidth, mHeight))

        result = clips_array(repo)
        result.write_videofile(output)

class MontagemMidnight(Montagem):
    def __init__(self):
        super().__init__()
        pass
    def compile(self, output):
        mWidth = 0
        mHeight = 0

        for video in self.repo:
            width = video.size[0]
            height = video.size[1]
            if width > mWidth:
                mWidth = width
            if height > mHeight:
                mHeight = height

        totaltime = 0
        for video in self.repo:
            totaltime += video.duration

        repo = []
        for video in self.repo:
            repo.append(video.resize((width, height)))

        cont = -1
        repo2 = []
        for video in self.repo:
            cont += 1
            
            itfreeze = cvsecs(0.1)
            ftfreeze = cvsecs(video.duration-0.1)
            i_im_freeze = video.to_ImageClip(itfreeze).fx(vfx.blackwhite)
            f_im_freeze = video.to_ImageClip(ftfreeze)

            before = True
            fconcat = []
            for _video in self.repo:
                if video == _video:
                    fconcat.append(video)
                elif before:
                    fconcat.append(i_im_freeze.set_duration(_video.duration))
                else:
                    fconcat.append(f_im_freeze.set_duration(_video.duration))
            concat = concatenate_videoclips(fconcat)
            repo2.append([concat])

        result = clips_array(repo2)
        result.write_videofile(output)








class Config:
    OUTPUT = 'videos'