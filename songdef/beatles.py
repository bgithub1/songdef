'''
Created on Apr 6, 2020

# create songdef's for Beatles tunes
@author: bperlman1
'''

# from songdef.songdef import Measure,Major,Minor,Major7,Minor7
# from songdef.songdef import Minor7f5,Dom7,Song,SongPart,Emb
from songdef import *
import songdef
from PIL._imagingmath import and_I

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
    acr_univ = Song([acr_univ_verse,acr_univ_chorus],title='Across The Universe')
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
    all_you_need_is_love = Song([all_you_need_is_love_intro,all_you_need_is_love_verse,all_you_need_is_love_chorus],
                                title='All You Need Is Love')
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
    
    and_i_love_her = Song([intro,verse1,chorus1,verse2],title="And I Love Her")
    return and_i_love_her    

def baby_your_a_rich_man():
    d5 = Diac5()
    c7fd = Dim(7,shfl=SharpFlat.FLAT)
    c5 = Diatr5()
    c4 = Diatr4()
    c1 = Diatr1()
    d5ov7 = Dom7(5,bass_num=7)
    covg = Chord(1,bass_num=5)
    intro1 = SongPart([Measure(c) for c in [d5,covg]*4],'intro1')
    verse1_chs = [c5,covg,d5] + [d5,d5,[(c4,16),(d5,16)],c1]*2 + [c5,c1,c5] + [d5,d5,[(c4,16),(d5,16)],c1]*2 
    verse1_measures = [Measure(c) for c in verse1_chs]
    verse1 = SongPart(verse1_measures,part_type='verse1')
    chorus1_chs = [c5,c1,c5,c1,[(c7fd,16),(d5ov7,16)],c1,d5,c1]
    chorus1_measures = [Measure(c) for c in chorus1_chs] * 2
    chorus1 = SongPart(chorus1_measures,'chorus1')
    return Song([intro1,verse1,chorus1], title="Baby You're a Rich Man")

def babys_in_black():
    intro = SongPart([Measure([(Diatr1(),6),(Diatr5(),6),(Diatr1(),12)],beats=24)],
                     part_type='intro')
    # verse1
    m1 = [(Diatr1(),12),(Diac5(),12)]
    m2 = [(Dom7(4),12),(Diac5(),12)]
    m3 = [(Diatr1(),6),(Diatr4(),6),(Diatr1(),6),(Diatr5(),6)]
    m4 = [(Diatr1(),24)]
    m5 = [(Dom7(1),12),(Diatr4(),12)]
    m6 = [(Diatr4(),12),(Diatr1(),6),(Diac5(),6)]
    m7 = [(Diatr1(),24)]
    verse1 = SongPart([Measure(chords,beats=24) for chords in [m1,m2,m3,m4,m5,m6,m7]],
                      part_type='verse1')
    
    # chorus1
    c1 = [(Diac6(),12),(Dom7(2),12)]
    c2 = [(Diatr4(),12),(Diac5(),12)]
    c3 = [(Diatr1(),12),(Diac5(),12)]
    c4 = [(Dom7(4),12),(Diac5(),12)]
    c5 = [(Diatr1(),6),(Diatr4(),6),(Diatr1(),6),(Diatr5(),6)]
    c1_c5 = [c1,c2,c3,c4,c5]
    c6 = [(Diatr1(),12),(Diatr5(),12)]
    c7 = [(Dom7(4),12),(Diac5(),12)]
    c8 = [(Diatr1(),6),(Diatr4(),6),(Diatr1(),12)]
    c6_c8 = [c6,c7,c8]
    c9_c13 = c1_c5
    c14_c17 = [m4,m5,m6,m7]
    
    c_all_chords = c1_c5 + c6_c8 + c9_c13 + c14_c17
    chorus1 = SongPart([Measure(chords,beats=24) for chords in c_all_chords],
                      part_type='chorus1')
    v2_1 = m1
    v2_2 = m2
    v2_3 = [(Diatr1(),6),(Dom7(4),6),(Diatr1(),12)]
    verse2 = SongPart([Measure(chords,beats=24) for chords in [v2_1,v2_2,v2_3]],
                      part_type='verse2')
    
    r = Song([intro,verse1,chorus1,verse2],title="Baby's In Black")
    return r    


def because():
    intro_chords = [Diac6(),Diac6(),Minor7f5(4,shfl=SharpFlat.SHRP),Dom7(7),Diatr1(),
               Diac6(),Dom7(1),Dom7(1,emb2=Emb(13)),Diatr4(),Dim(4)]
    intro = SongPart([Measure(c) for c in intro_chords],part_type='intro')
    # verse1
    verse1 = SongPart([Measure(c) for c in intro_chords],part_type='verse1')
    verse2 = SongPart([Measure(c) for c in intro_chords],part_type='verse2')
    c_chords = [Diatr6(),Diatr6(),Dom7(7),Dom7(7),Diatr4(),Dim(4)]
    chorus1 = SongPart([Measure(c) for c in c_chords],part_type='chorus1')
    ending = SongPart([Measure(c) for c in intro_chords],part_type='ending')
    r = Song([intro,verse1,verse2,chorus1,ending],title="Because")
    return r

    

_all_songs = [(across_the_universe(),'D'),
              (all_you_need_is_love(),'G'),
              (and_i_love_her(),'E'),
              (baby_your_a_rich_man(),'C'),
              (babys_in_black(),'A'),
              (because(),'A')
               ]


if __name__=='__main__':
    all_you_need_is_love().print_song('G')
    
#     for s in _all_songs:
#         s[0].print_song(s[1])
#         print('.')
#         print('.')
#         print('.')

