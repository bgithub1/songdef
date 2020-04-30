'''
Created on Apr 6, 2020

# create songdef's for Beatles tunes
@author: bperlman1
'''

# from songdef.songdef import Measure,Major,Minor,Major7,Minor7
# from songdef.songdef import Minor7f5,Dom7,Song,SongPart,Emb
from songdef import *
import songdef
import copy
from nis import match


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


def blackbird():
    introchs = [Measure([(Diatr1(),8),(Diatr2(),8),(Major(1,bass_num=3),8)],24),
                Measure(Diatr1())]
    intro = SongPart(introchs,part_type='intro')
    
    v1_1 = Measure([(Diatr1(),8),(Diatr2(),8),(Major(1,bass_num=3),8)],24)
    v1_2 = Measure(Diatr1())
    v1_3 = Measure([
                    (Diatr4(),8),
                    (Dom7(2,bass_num=4,bass_shfl=SharpFlat.SHRP),8),                 
                    (Diac5(),8),
                    (Dom7(3,bass_num=5,bass_shfl=SharpFlat.SHRP),8)
    ])
    v1_4 = Measure([
        (Diatr6(),16),
        (Minor(4,bass_num=6,bass_shfl=SharpFlat.FLAT),16)
    ])
    v1_5 = Measure([
        (Major(1,bass_num=5),8),
        (Dom7(2,bass_num=4,bass_shfl=SharpFlat.SHRP),8),                 
        (Minor7(2,bass_num=4),16),
        (Minor(4),16)
    ])
    v1_6 = Measure([
        (Major(1,bass_num=3),16),
        ((Dom7(2)),16),
        ((Minor7(2,bass_num=5)),8),
        ((Diac5()),8)
    ])
    v1_1_6 = [v1_1,v1_2,v1_3,v1_4,v1_5,v1_6]
    
    v1_7 = Measure([
        ((Diatr1()),16),
        ((Diatr4()),8),
        ((Major(1,bass_num=3)),8)
    ])
    v1_8 = Measure([
        ((Dom7(2)),16),
        ((Diac5()),16)
    ])
    v1_9 = Measure((Diatr1(),16))
    verse1 = SongPart(v1_1_6 + [v1_7,v1_8,v1_9],part_type='verse1')
    
    # verse2
    v2_7 = v2_7 = Measure((Diatr1(),16))
    verse2 = SongPart(v1_1_6 + [v2_7],part_type='verse2')
    
    # chorus
    c1 = Measure([
        (Major(7,shfl=SharpFlat.FLAT),8),
        (Major(4,bass_num=6),8),
        (Minor(5),8),
        (Diatr4(),8)
    ])
    c2 = Measure([
        (Major(3,shfl=SharpFlat.FLAT),16),
        (Diatr4(),16),
    ])
    c3 = c1
    c4 = Measure([
        (Major(3,shfl=SharpFlat.FLAT),16),
        (Dom7(2),16),
    ])
    c5 = Measure(Diac5(),16)
    c6 = Measure([
        (Diatr1(),8),
        (Dom7(2),8),
        (Major(1,bass_num=3),8),
    ])
    c7 = Measure(Diatr1())
    c8 = v1_3
    c9 = v1_4
    c10 = Measure([
        (Major7(1,bass_num=5),8),
        (Dom7(2,bass_num=4,bass_shfl=SharpFlat.SHRP),8),
        (Minor7(2,bass_num=4),16),
        (Minor(4),8)
    ])
    c11 = Measure([
        (Major(1,bass_num=3),16),
        (Dom7(2),16),
        (Diac5(),16)
    ])
    c12 = Measure((Diatr1(),16))
    c1_12 = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]
    c13_21  = [c1,c2,c3,c4,c5,c6,c8,c8,c8]
    
    c22 = Measure([(Diatr1(),8),(Dom7(2),8),(Major(1,bass_num=3),8)],24)
    c23 = Measure([(Diatr4(),8),(Major(1,bass_num=3),8),(Dom7(2),8)])
    c24 = Measure(Minor7(2,bass_num=5))
    c_all_chords = c1_12 + c13_21 + [c22,c23,c24]
    chorus1 = SongPart(c_all_chords,part_type='chorus2')
    
    v3_1_5 = [v1_1,v1_2,v1_3,v1_4,v1_5]
    v3_6 = Measure([
        (Major(1,bass_num=3),16),
        (Dom7(2),16)
    ])
    v3_7 = Measure([
        (Minor7(2,bass_num=5),8),
        (Diac5(),8),
        (Diatr1(),16)
    ])
    v3_8 = Measure([
        (Diatr4(),8),
        (Major(1,bass_num=3),8),
        (Dom7(2),16)
    ])
    v3_9 = v3_7
    # [v3_8,v3_9] gets repeated 2 times at end
    verse3 = SongPart(v3_1_5 + [v3_6,v3_7] + [v3_8,v3_9] * 2,part_type = "verse3")
    
    b = Song([intro,verse1,verse2,chorus1,verse3],title="Blackbird")
#     blackbird.print_song('G')
    return b       

def cant_buy_me_love():
    intro_chords = [Diatr3(),Diatr6(),Diatr3(),Diatr6(),Diac2(),Diatr5()]
    intro = SongPart([Measure(c) for c in intro_chords],part_type='intro')
    v1_1 = [Measure(Diatr1()) for _ in range(4)]
    v1_2 = [Measure(Dom7(4)),Measure(Dom7(4)),Measure(Diatr1()),Measure(Diatr1())]
    v1_3 = [Measure(Dom7(5)),Measure(Dom7(4)),Measure(Dom7(4)),Measure(Diatr1())]
    verse1 = SongPart(v1_1+v1_2+v1_3,'verse1')
    verse2 = SongPart(v1_1+v1_2+v1_3,'verse2')
    ch1 = [Diatr3(),Diatr6(),Diatr1(),Diatr1()]
    ch2 = [Diatr3(),Diatr6(),Diatr4(),Diatr5()]
    chorus1 = SongPart([Measure(c) for c in ch1+ch2],'chorus1')
    verse3 = SongPart(v1_1+v1_2+v1_3,'verse3')
    instrumental = SongPart(v1_1+v1_2+v1_3,'instrumental')
    chorus2 = SongPart([Measure(c) for c in ch1+ch2 +[Diatr1()]],'chorus2')
    cbml = Song([intro,verse1,verse2,chorus1,verse3,instrumental,chorus2],title="Can't Buy Me Love")
#     cbml.print_song('C')
    return cbml

def come_together(): 
    # come together
    intro_chords = [Minor7(1) for _ in range(4)]
    intro1 = SongPart([Measure(c) for c in intro_chords],'intro1')
    v1_1_chords = intro_chords + [Diatr5(),Diatr5(),Dom7(4),Dom7(4)]
    v1 = SongPart([Measure(c) for c in v1_1_chords ],'verse1')
    intro2 = SongPart([Measure(c) for c in intro_chords],'intro2')
    v2_end_m1 = Measure([(Diatr6(),24),(Minor(6,bass_num=5),8)])
    v2_end_m2 = Measure([(Diatr4(),16),(Major(4,bass_num=5),16)])
    v2_end = [v2_end_m1,v2_end_m2]
    v2 = SongPart([Measure(c) for c in v1_1_chords] + v2_end ,'verse2')
    intro3 = SongPart([Measure(c) for c in intro_chords],'intro3')
    v3 = SongPart([Measure(c) for c in v1_1_chords] + v2_end ,'verse3')
    intro4 = SongPart([Measure(c) for c in intro_chords],'intro4')
    v4 = SongPart([Measure(c) for c in v1_1_chords] + v2_end ,'verse4')
    ct = Song([intro1,v1,intro2,v2,intro3,v3,intro4,v4],title='Come Together')
#     ct.print_song('D')
    return ct       


def day_in_the_life():
    # day in the life
    
    intro = SongPart([
        Measure([(Diatr1(),16),(Diatr3(),16)]),
        Measure([(Diatr6(),16),(Diac6(),16)]),
        Measure(Diatr4()),Measure(Diatr4())
    ],'intro')
    v1_1_measures = [
        Measure([(Diatr1(),16),(Minor(3,bass_num=7),16)]),
        Measure(Diatr6()),
        Measure([(Diatr4(),16),(Minor(6,bass_num=3),16)]),
        Measure([(Diatr2(),16),(Diac4(),16)]),
        Measure([(Diatr1(),16),(Diatr3(),16)]),
        Measure(Diatr6()),
        Measure([(Diatr4(),16),(Major(7,shfl=SharpFlat.FLAT),16)]),
        Measure([(Minor(6),16),(Minor(6,bass_num=5),16)]),
        Measure([(Diatr4(),16),(Major(7,shfl=SharpFlat.FLAT),16)]),
    ]
    v1_2_measures = [Measure([(Minor(6),16),(Diac4(),16)])]
    
    v1 = SongPart(v1_1_measures + v1_2_measures,'verse1')
    v2_2_measures = [Measure(Diatr4())]
    v2 = SongPart(v1_1_measures + v2_2_measures,'verse2')
    v3 = SongPart(v1_1_measures + v2_2_measures,'verse3')
    turn_you_on_1 = SongPart([
        Measure([(Diatr4(),16),(Minor(3,bass_num=7),16)]),
        Measure([(Diatr1(),16),(Minor(6,bass_num=5),16)]),
        Measure(Major(6)),Measure(Major(6))
    ],'turn_you_on_1')
    got_up_1 = SongPart([
        Measure(Major(6)),Measure([(Major(6),16)],beats=16),
        Measure(Diatr5()),
        Measure([(Major(6),16),(Minor7(7,bass_num=3),16)]),
        Measure([(Major(6),16),(Minor7(7,bass_num=3),16)]),
        Measure(Minor7(7,bass_num=3)),
    ],'got_up_1')
    got_up_2 = SongPart([
        Measure(Major(6)),Measure([(Major(6),16)],beats=16),
        Measure(Diatr5()),
        Measure([(Major(6),16),(Minor7(7,bass_num=3),8),(Dom7(3),8)]),
        Measure([(Major(6),16),(Minor7(7,bass_num=3),16)]),
    ],'got_up_2')
    ah_chords = [Diatr4(),Diatr1(),Diatr5(),Major(2),Major(6),
                Diatr4(),Diatr1(),Diatr5(),Major(2),Major(2)]
    ah_ah_ah_ah = SongPart([Measure(c) for c in ah_chords] ,'ah_ah_ah_ah')
    v4 = v3 = SongPart(v1_1_measures + v2_2_measures,'verse4')
    turn_you_on_2 = copy.deepcopy(turn_you_on_1)
    turn_you_on_2.part_type = 'turn_you_on_2'
    aditl = Song([intro,v1,v2,v3,turn_you_on_1,got_up_1,got_up_2,ah_ah_ah_ah,v4,turn_you_on_2],title="A Day In The Life")
#     aditl.print_song('G')    
    return aditl


def day_tripper():
                # day tripper
    intro = SongPart([Measure(Dom7(1)) for _ in range(6)],'intro')
    v1_0 = [Measure(Dom7(1)) for _ in range(4)]
    v1_1 = [Measure(Dom7(1)) for _ in range(4)]
    v1_2 = [Measure(Dom7(4)) for _ in range(2)]
    v1_3 = [Measure(Dom7(1)) for _ in range(2)]
    v1_4 = [Measure(Dom7(2)) for _ in range(4)]
    v1_5 = [Measure(c) for c in [Dom7(4),Dom7(3),Dom7(6),Dom7(5)]]
    v1 = SongPart(v1_0+v1_1+v1_2+v1_3+v1_4+v1_5,'verse1')
    v2 = copy.deepcopy(v1)
    v2.part_type='verse2'
    v3 = copy.deepcopy(v1)
    v3.part_type='verse3'
                
    dtrip = Song([intro,v1,v2,v3],title='Day Tripper')
#     dtrip.print_song('E')
    return dtrip
_all_songs = [(across_the_universe(),'D'),
              (all_you_need_is_love(),'G'),
              (and_i_love_her(),'E'),
              (baby_your_a_rich_man(),'C'),
              (babys_in_black(),'A'),
              (because(),'A'),
              (blackbird(),'G'),
              (cant_buy_me_love(),'C'),
              (come_together(),'D'),
              (day_in_the_life(),'G'),
              (day_tripper(),'E')
               ]


if __name__=='__main__':
#     all_you_need_is_love().print_song('G')
    
    for s in _all_songs:
        s[0].print_song(s[1])
        print('.')
        print('.')
        print('.')
    
    chord_pattern = [Major(1),Major(5),Minor(6)]
    for song,key in _all_songs:
        match_array = song.find_song_pattern(chord_pattern)
        if len(match_array)>0:
            print(song.title)
            for pattern in match_array:
                print([c.to_string(key) for c in pattern])
        
