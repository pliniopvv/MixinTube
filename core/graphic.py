from textual.widgets import Button, Label, Header, Footer, LoadingIndicator, ProgressBar
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Center, VerticalGroup
from core import group_by

import asyncio
from threading import Thread

class MixinApp(App):
    CSS_PATH = "graphic.tcss"


    def __init__(self, lista):
        super().__init__()

        ordened = group_by(lista);

        self.list = lista
        self.ordened = ordened

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        list = self.ordened
        
        for key in list:
            yield Center(Label(list[key][0].root), classes="title")
            for video in list[key]:
                yield VideoView(video)

    # def compose(self) -> ComposeResult:
    #     yield Header()
    #     yield Footer()

    #     for video in self.list:
    #         yield VideoView(video)

class VideoView(HorizontalGroup):
    def __init__(self, video):
        super().__init__()
        self.video = video

    def updateProgress(self, total, progress):
        bar = self.query_one(ProgressBar)
        bar.update(total=total, progress=progress)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        id = event.button.id
        
        if id == "root":
            thread = Thread(target=self.video.download, args=[self.updateProgress])
            thread.start()
        elif id == "cut":
            asyncio.run(self.video.download_cut(self.updateProgress))
            # self.query_one("cut").disabled = True
        self.refresh()

    def compose(self) -> ComposeResult:
        video = self.video

        rootdownloaded = video.rootExists()
        cut_exists = video.exists()

        if rootdownloaded:
            yield Button.success("Root", disabled=rootdownloaded, id="root")
        else:
            yield Button.error("Root", disabled=rootdownloaded, id="root")

        if cut_exists:
            yield Button.success("Cut", disabled=cut_exists, id="cut")
        else:
            yield Button.error("Cut", disabled=cut_exists, id="cut")
        
        yield VerticalGroup(
            # Label(video.root),
            Label(video.descricao),
            ProgressBar(total=100, show_percentage=0)
        )
        # yield Center(Label(video.root))
        # yield Center(Label(video.descricao))