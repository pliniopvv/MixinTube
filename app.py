from core import parse_roteiro
from core.graphic import MixinApp

if __name__ == "__main__":
    lista = parse_roteiro("raw/repo/geral.raw")

    app = MixinApp(lista)
    app.run()