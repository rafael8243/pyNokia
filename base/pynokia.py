import pandas as pd
import os
from time import perf_counter

import nok_etreader as nokr

def open_file():
    #caminho = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\dump_sample.xml"
    #caminho = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\Dump_20220927_2G_RBA.xml"
    caminho = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\Dump_20211001_3G_RBA.xml" #213MB

    print(f'File Size is {round(os.stat(caminho).st_size / (1024 * 1024),2)} MB')

    return caminho


if __name__ == '__main__':

    t_start = perf_counter()

    caminho = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\output\\"

    nokr.process(open_file(), caminho)

    t_end = perf_counter()
    t_delta = round(t_end - t_start , 2)
    print('\nTempo total:', t_delta,'s')