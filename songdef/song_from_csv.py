'''
Created on Apr 30, 2020

@author: bperlman1
'''
import pandas as pd
import numpy as np
import copy
import sys,os
# if os.path.abspath('..') not in sys.path:
#     sys.path.append(os.path.abspath('..'))
# if os.path.abspath('.') not in sys.path:
#     sys.path.append(os.path.abspath('.'))    
import songdef as sd 


if __name__== '__main__':
#     c = sd.Chord(1,bass_num=7,bass_shfl=sd.SharpFlat.FLAT)
#     print(c.to_string('D'))
    song_def = input('Enter Song Name xlsx File w/o the xlsx, followed by a key (e.g.: all_my_loving,E): ' )
    if song_def is not None and len(song_def)>0:
        song_name,key = song_def.split(',')
        df_song = pd.read_excel(f'./songxlsx/{song_name}.xlsx',sheet_name='songcsv')
        sd.song_from_csv(df_song,song_name).print_song(key)
    
    