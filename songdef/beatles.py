'''
Created on Apr 6, 2020

# create songdef's for Beatles tunes
@author: bperlman1
'''

# from songdef.songdef import Measure,Major,Minor,Major7,Minor7
# from songdef.songdef import Minor7f5,Dom7,Song,SongPart,Emb
from songdef import *

def across_the_universe():
    # main verse
    m1 = Measure(Major(1))
    m2 = Measure(Minor7(3))
    m3 = Measure(Minor7(2))
    m4 = Measure([(Major(5),16),(Dom7(5),16)])
    m3_min = Measure([(Minor7(2),16),(Minor(4),16)])
    acr_univ_verse = SongPart([m1,m2,m3,m4,m1,m2,m3_min],part_type='verse')
    
    # chorus
    chm_1 = m1
    twomin7_b5 = Minor7(2)
    twomin7_b5.bass_num = 5
    four_b1 = Major(4,bass_num=1)
    chm_1 = m1
    chm_2 = m1
    chm_3 = Measure(twomin7_b5)
    chm_4 = Measure(Dom7(5))
    chm_5 = Measure(Dom7(5))
    chm_6 = Measure(four_b1)
    chm_7 = m1
    chm_8 = Measure(Dom7(5))
    chm_9 = chm_8
    chm_10 = Measure(four_b1)
    chm_11 = m1
    
    acr_univ_chorus = SongPart([chm_1,chm_2,chm_3,chm_4,chm_5,chm_6,chm_7,chm_8,chm_9,chm_10,chm_11],part_type='chorus')
    acr_univ = Song([acr_univ_verse,acr_univ_chorus])
    acr_univ.print_song('D')
    return acr_univ


def all_you_need_is_love():
    m1 = Measure([(Major(1),16),(Major(5,bass_num=7),16)])
    m2 = Measure(Minor(6))
    m3 = m1
    m4 = m2
    m5 = Measure([(Dom7(5,bass_num=2),16),(Major(1),16)])
    m6 = Measure([(Dom7(5,bass_num=7),16),(Dom7(5,emb2=Emb(9),bass_num=6),16)])
    m7 = Measure([(Dom7(5),16),(Dom7(5,bass_num=4),16)])
    m8 = Measure(Dom7(5))
    all_you_need_is_love_intro = SongPart([m1,m2,m3,m4,m5,m6,m7,m8],part_type='intro')
    all_you_need_is_love_verse = SongPart([m1,m2,m3,m4,m5,m6,m7,m8],part_type='verse')

    ch1 = Measure([(Major(1),16),(Dom7(2,emb2=Emb(4)),16)])
    ch2 = Measure(Dom7(5))
    ch3 = ch1
    ch4 = ch2
    ch5 = Measure([(Major(1),16),(Dom7(3),16)])
    ch6 = Measure([(Minor(6),16),(Major(1,bass_num=5),16)])
    ch7 = Measure([(Major(4),16),(Dom7(5),16)])
    all_you_need_is_love_chorus = SongPart([ch1,ch2,ch3,ch4,ch5,ch6,ch7],'chorus')
    all_you_need_is_love = Song([all_you_need_is_love_intro,all_you_need_is_love_verse,all_you_need_is_love_chorus])
    return all_you_need_is_love


def and_i_love_her():
    # intro
    intro = SongPart([
            Measure(Diac2()),Measure(Diac2()),Measure(Sixth(1)),Measure(Sixth(1)),
            Measure(Diac2()),Measure(Diac2()),Measure(Sixth(1)),Measure(Sixth(1))
        ],
        part_type='intro'
    )
    
    verse1_measures = [
        Measure(Diac2()),Measure(Diac6()),
        Measure(Diac2()),Measure(Diac6()),
        Measure(Diac2()),Measure(Diac6()),
        Measure(Diatr4()),Measure(Diac5()),
        Measure(Sixth(1)),Measure(Sixth(1))
    ]
    
    verse1 = SongPart(verse1_measures + verse1_measures,part_type='verse1')
    
    chorus1_measures = [
        Measure(Diac6()),Measure(Diatr5()),
        Measure(Diac6()),Measure(Diatr3()),
        Measure(Diac6()),Measure(Diatr3()),
        Measure(Diatr5()),Measure(Diatr5()),
    ]
    chorus1 = SongPart(chorus1_measures,part_type='chorus1')
    
    verse2 = SongPart(verse1_measures,part_type='verse2')
    
    and_i_love_her = Song([intro,verse1,chorus1,verse2])
    return and_i_love_her    


if __name__=='__main__':
    print("------------- ACROSS THE UNIVERSE -------------------")
    across_the_universe().print_song('D')
    print('.')
    print('.')
    print('.')
    print("------------- ALL YOU NEED IS LOVE -------------------")
    all_you_need_is_love().print_song('G')
    print('.')
    print('.')
    print('.')
    print("------------- AND I LOVE HER -------------------")
    and_i_love_her().print_song('E')
    print('.')
    print('.')
    print('.')
    
    