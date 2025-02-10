from pyffmpeg import FFmpeg
import time

entrada = "renam_mbl_ta_autorizado_bater_em_quem_procura.mp4"
saida = "renam_mbl_ta_autorizado_bater_em_quem_procura.webm"

def handle_progress(val):
    print("#####")
    breakpoint()
    print(val)
    print("#####")

ff = FFmpeg()
ff.loglevel = 'CRITICAL'
ff.report_progress = True
ff.onProgressChanged = handle_progress
ff.convert(entrada, saida)
ff = None
time.sleep(2)