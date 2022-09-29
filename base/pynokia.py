from time import perf_counter
import pandas as pd
#import resource
import os

class ConfigFile:
    file_source = 1

import nok_reader as nokr

def open_file():
    caminho = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\dump_sample.xml"
    #caminho = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\Dump_20220923_3G_RBA.xml"

    print(f'File Size is {round(os.stat(caminho).st_size / (1024 * 1024),2)} MB')

    return open(caminho)


if __name__ == '__main__':

    t_start = perf_counter()

    opt_list4 = set(('LNCEL_FDD', 'LNBTS', 'LNADJ', 'LNCEL', 'LNREL', 'IRFIM', 'SIB', 'LNADJL', 'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'LNBTS_FDD'))
    opt_list3 = set(('ADJI', 'WBTS', 'ADJS', 'ADJD', 'WCEL', 'ADJG', 'ADJL', 'RNC'))
    opt_list2 = set(('LAPD', 'MAL', 'TRX', 'BCF', 'ADJL', 'DAP', 'BTS', 'CSDAP', 'ADCE', 'ADJW', 'BAL', 'BSC'))
        
    with open_file() as file:
        count = 0

        mo_set = set()
        param_dict = dict()
        esse_mo = ''
        
        for line in file:

            esse_mo = nokr.process(line, mo_set, param_dict, esse_mo)
            count += 1
    
    #print('Peak Memory Usage =', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    #print('User Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_utime)
    #print('System Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_stime)

    print(mo_set)

    t_end = perf_counter()
    t_delta = round(t_end - t_start,2)
    print(t_delta,'segundos')