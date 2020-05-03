#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from enum import Enum
import copy
import pdb
import inspect



_SHARP = '#'
_FLAT = 'f'
_PLUS = '+'
_FSP = [_FLAT,_SHARP,_PLUS]
_SHARP_FLAT = _SHARP+_FLAT
_FLAT_SHARP = _FLAT+_SHARP


# define keys using circle of 4ths
KEYS = {
    'C':['C','D','E','F','G','A','B'],
    'F':['F','G','A','Bf','C','D','E'],
    'Bf':['Bf','C','D','Ef','F','G','A'],
    'Ef':['Ef','F','G','Af','Bf','C','D'],
    'Af':['Af','Bf','C','Df','Ef','F','G'],
    'Df':['Df','Ef','F','Gf','Af','Bf','C'],
    'Gf':['Gf','Af','Bf','Cf','Df','Ef','F'],
    'B':['B','C#','D#','E','F#','G#','A#'],
    'E':['E','F#','G#','A','B','C#','D#'],
    'A':['A','B','C#','D','E','F#','G#'],
    'D':['D','E','F#','G','A','B','C#'],
    'G':['G','A','B','C','D','E','F#'],
}

def next_note(key,note,up_down=1):
    key2 = key[0].upper() 
    if len(key)>1:
        # there may be a sharp or flat
        key2 = key2 + key[1]
    
    key_array = KEYS[key.upper()]
    i = key_array.index(note) + up_down
    if i > 7:
        next_i = 1
    elif i<1:
        next_i = 7
    return key_array[i]

class MajMin(Enum):
    MIN = 1
    MAJ = 2
    DIM = 3
    def __str__(self):
        return self.name

class SharpFlat(Enum):
    FLAT=1
    SHRP=2
    PLUS=3
    def __str__(self):
#         return _SHARP if self.value==2 else _FLAT
        return _FSP[self.value-1]

class Emb():
    def __init__(self,emb_num: int,shfl: SharpFlat=None):
        self.emb_num = emb_num
        self.shfl = shfl
    def __str__(self):
        r = str(self.emb_num)
        if self.shfl is not None:
            r = str(self.shfl)+r
        return r
    def is_emb(self,other):
        if (type(other)==Emb) or (issubclass(type(other),Emb)):
            return True
        raise ValueError(f"Emb.is_emb: str(other) is not type or subclass of Emb")
    
    def value(self):
        return self.emb_num * 10 + (0 if self.shfl is None else self.shfl.value)
    
    def _gtlteq(self,other):
#         self_emb = self.emb_num * 10 + (0 if self.shfl is None else self.shfl.value)
#         other_emb = other.emb_num * 10 + (0 if other.shfl is None else other.shfl.value)
        self_emb = self.value()
        other_emb = other.value()
        if self_emb == other_emb:
            return 0
        if self_emb > other_emb:
            return 1
        if self_emb < other_emb:
            return 2
        
    def __lt__(self,other):
        gtlteq = self._gtlteq(other)
        if gtlteq == 2:
            return True
        return False
    def __le__(self,other):
        gtlteq = self._gtlteq(other)
        if (gtlteq == 0) or (gtlteq == 2):
            return True
        return False
    def __gt__(self,other):
        gtlteq = self._gtlteq(other)
        if gtlteq == 1:
            return True
        return False
    def __ge__(self,other):
        gtlteq = self._gtlteq(other)
        if (gtlteq == 0) or (gtlteq == 1):
            return True
        return False
    def __eq__(self,other):
        gtlteq = self._gtlteq(other)
        if (gtlteq == 0):
            return True
        return False
    def __ne__(self,other):
        return not self.__eq__(other)

def handle_double_shfl(note_string):
    ns = note_string
    fs = _FLAT+_SHARP
    sf = _SHARP+_FLAT
    ss  = _SHARP+_SHARP
    ff = _FLAT+_FLAT
    if fs in note_string:
        ns = note_string.replace(fs,'')
    elif sf in note_string:
        ns = note_string.replace(sf,'')
    elif ss in note_string:
        n = note_string[0]
        # move n to the next letter in the key of C
        cnotes = KEYS['C']
        cindex = cnotes.index(n)
        new_cindex = 0 if cindex>=7 else cindex+1
        new_n = cnotes[new_cindex]
        ns = note_string.replace(n+ss,new_n)
    elif ff in note_string:
        n = note_string[0]
        # move n to the next letter in the key of C
        cnotes = KEYS['C']
        cindex = cnotes.index(n)
        new_cindex = 7 if cindex<=0 else cindex-1
        new_n = cnotes[new_cindex]
        ns = note_string.replace(n+ff,new_n)
    return ns
        
# maps for 
DICT_MAJMIN = {'+':MajMin.MAJ,'-':MajMin.MIN,'d':MajMin.DIM,'none':None,'nan':None}
DICT_SHFL = {'-':SharpFlat.FLAT,'+':SharpFlat.SHRP,'none':None,'nan':None}
        
class Chord():
    def __init__(self,
                 chnum: int,
                 shfl: SharpFlat=None,
                 majmin: MajMin=None,
                 emb1: Emb=None,
                 emb2: Emb=None,
                 bass_num: int=None,
                 bass_shfl: SharpFlat=None):
        self.chnum = chnum
        self.shfl = shfl
        self.majmin = majmin
        self.emb1 = emb1
        self.emb2 = emb2
        self.bass_num = bass_num
        self.bass_shfl = bass_shfl
            
    def to_string(self,key=None):
        bass_note = None if ((key is None) or (self.bass_num is None)) else KEYS[key][self.bass_num-1]
        bass_note = '/' + bass_note if bass_note is not None else ''
        bass_shfl = str(self.bass_shfl) if self.bass_shfl is not None else ''
        bn = bass_note + bass_shfl
        bn = bn.strip()
        bn = bn.replace(_SHARP_FLAT,'').replace(_FLAT_SHARP,'')
        emb1 = str(self.emb1) if self.emb1 is not None else ''
        emb2 = str(self.emb2) if self.emb2 is not None else ''
#         chn = self.chnum if self.chnote is None else self.chnote
        mn = str(self.majmin) if self.majmin is not None else ''
        mn = mn.lower()
        # handle getting note
        shfl = '' if self.shfl is None else str(self.shfl)
        if key is None:
            chn = str(self.chnum + shfl)
        else:
            chn = KEYS[key][self.chnum-1]
            # handle sharp flat
            chn = handle_double_shfl(chn+shfl)
#             if self.shfl is not None:
#                 # case 1, the key is None
#                 if self.shfl == SharpFlat.FLAT:
#                     if _SHARP in chn:
#                         chn = chn.replace(_SHARP,'')
#                     elif _FLAT in chn:
#                         chn = next_note(key,chn,up_down=-1)
#                     else:
#                         chn = chn + str(self.shfl)
#                 elif self.shfl == SharpFlat.SHRP:
#                     if _SHARP in chn:
#                         chn = next_note(key,chn,up_down=1)
#                     elif _FLAT in chn:
#                         chn = chn.replace(_FLAT,'')
#                     else:
#                         chn = chn + str(self.shfl)
                        
        r =  f"{chn}{mn}{emb1}{emb2}{bn}".strip()
        return r
    def _isChord(self,other):
        if not (type(other)==Chord or issubclass(type(other),Chord)):
            raise ValueError("Chord.__lt__: other is not a type or subclass of Chord")
    
    def _issupersetof(self,other):
        self._isChord(other)
        attributes = ['chnum','shfl','majmin','emb1','emb2','bass_num']
        attr_self = [getattr(self,a) for a in attributes]
        attr_other = [getattr(other,a) for a in attributes]
        r = all([attr_self[i]==attr_other[i] for i in range(len(attributes)) if attr_other[i] is not None])
        return r
    
    def _gtlteq(self,other):
        '''
        return True if lt, False if gt or None if eq
        '''
        self._isChord(other)
        if other.chnum < self.chnum:
            return True
        elif other.chnum > self.chnum:
            return False
        # chnu is ==
        
        other_shfl = 0 if other.shfl is None else other.shfl.value
        self_shfl =  0 if self.shfl is None else self.shfl.value
        if other_shfl < self_shfl: 
            return True
        elif other_shfl > self_shfl: 
            return False
        # shfl's are ==
        
#         other_majmin = 0 if other.majmin is None else other.majmin.value
        if other.majmin is None:
            other_majmin = 0
        elif other.majmin ==3:
            other_majmin = -1
        else:
            other_majmin = other.majmin.value
            
#         self_majmin = 0 if self.majmin is None else self.majmin.value
        if self.majmin is None:
            self_majmin = 0
        elif self.majmin ==3:
            self_majmin = -1
        else:
            self_majmin = self.majmin.value

        if other_majmin < self_majmin:
            return True
        elif other_majmin > self_majmin:
            return False
        # majmin's are ==
        
        other_emb1 = 0 if other.emb1 is None else other.emb1
        self_emb1 = 0 if self.emb1 is None else self.emb1
        if other_emb1 < self_emb1:
            return True
        elif other_emb1 > self_emb1:
            return False
        # emb1's are ==

        other_emb2 = 0 if other.emb2 is None else other.emb2.value()
        self_emb2 = 0 if self.emb2 is None else self.emb2.value()
        if other_emb2 < self_emb2:
            return True
        elif other_emb2 > self_emb2:
            return False
        # emb2's are ==
        
        other_bass_num = 0 if other.bass_num is None else other.bass_num
        self_bass_num = 0 if self.bass_num is None else self.bass_num
        if other_bass_num < self_bass_num:
            return True
        elif other_bass_num > self_bass_num:
            return False
        # bass_num's are ==
        
        other_bass_shfl = 0 if other.bass_shfl is None else other.bass_shfl.value
        self_bass_shfl = 0 if self.bass_shfl is None else self.bass_shfl.value
        if other_bass_shfl < self_bass_shfl:
            return True
        elif other_bass_shfl > self_bass_shfl:
            return False
        # bass_shfl's are ==
        
        # all are equal
        return None 
    
    def __lt__(self,other):
        r = self._gtlteq(other)
        if (r is None) or r:
            return False
        return True
    def __le__(self,other):
        r = self._gtlteq(other)
        if (r is None) or not r:
            return True
        return False
    def __gt__(self,other):
        r = False if self.__le__(other) else True
        return r
    def __ge__(self,other):
        return False if self.__lt__(other) else True
    def __eq__(self,other):
        return True if self._gtlteq(other) is None else False
    def __ne__(self,other):
        return not self.__eq__(other)



class Major(Chord):
    def __init__(self,chnum,**kwargs):
        super(Major,self).__init__(chnum,**kwargs)
class Major7(Chord):
    def __init__(self,chnum,**kwargs):
        super(Major7,self).__init__(chnum,majmin=MajMin.MAJ,emb1=7,**kwargs)
class Dom7(Chord):
    def __init__(self,chnum,**kwargs):
        super(Dom7,self).__init__(chnum,emb1=7,**kwargs)
class Dim(Chord):
    def __init__(self,chnum,**kwargs):
        super(Dim,self).__init__(chnum,majmin=MajMin.DIM,**kwargs)
class Minor(Chord):
    def __init__(self,chnum,**kwargs):
        super(Minor,self).__init__(chnum,majmin=MajMin.MIN,**kwargs)
class Minor7(Chord):
    def __init__(self,chnum,**kwargs):
        super(Minor7,self).__init__(chnum,majmin=MajMin.MIN,emb1=7,**kwargs)
class Minor7f5(Chord):
    def __init__(self,chnum,**kwargs):
        super(Minor7f5,self).__init__(chnum,majmin=MajMin.MIN,emb1=7,emb2=Emb(5,shfl=SharpFlat.FLAT),**kwargs)
    
class Minorf5(Chord):
    def __init__(self,chnum,**kwargs):
        super(Minorf5,self).__init__(chnum,majmin=MajMin.MIN,emb2=Emb(5,shfl=SharpFlat.FLAT),**kwargs)

class Sixth(Chord):
    def __init__(self,chnum,**kwargs):
        super(Sixth,self).__init__(chnum,emb1=6,**kwargs)
    

class MeasureFraction():
    def __init__(self,chord:Chord,num_32nds:float=32):
        self.chord = chord
        self.num_32nds=num_32nds
    def to_string(self,key):
        chord = copy.deepcopy(self.chord)
#         chord.change_key(key)
#         chord.key = key
        
        l = "_" * self.num_32nds
        c = chord.to_string(key).replace(' ','')
        c = c + " " * (len(l) - len(c))
        c = c[0:len(l)]
        return f"{l}\n{c}"
        
class Measure():
    def __init__(self,measure_fraction_list: list=None,beats:int=32):
        # what kind of obect is measure_fraction_list
        self.measure_fraction_list = []
        if type(measure_fraction_list) == list or type(measure_fraction_list)==np.ndarray:
            for mf in measure_fraction_list:
                self.add_fraction(mf)
        else:
            # measure_fraction_list is a tuple, MeasureFraction instance, or a Chord
            self.add_fraction(measure_fraction_list)
        self.beats = beats
            
    def add_fraction(self,mf):
            if (type(mf) == MeasureFraction) or (issubclass(type(mf),MeasureFraction)):
                self.measure_fraction_list.append(mf)
            elif type(mf)==tuple:
                # it's a tuple
                self.measure_fraction_list.append(MeasureFraction(mf[0],mf[1] if len(mf)>1 else self.beats))
            elif (type(mf)==Chord) or (issubclass(type(mf),Chord)) :
                self.measure_fraction_list.append(MeasureFraction(mf))
            else:
                raise ValueError('Measure: invalid element in measure_fraction_list: {str(mf)}')
    def to_string(self,key):
        l = ''
        c = ''
        for m in self.measure_fraction_list:
            mp_str = m.to_string(key)
            mpsplits =  mp_str.split('\n')
            l = l + mpsplits[0]
            c = c + mpsplits[1]
        return f"{l}\n{c}"     
                
class SongPart():
    def __init__(self,measure_list:list,part_type='verse'):
        self.measure_list = measure_list
        self.part_type = part_type
        
    def song_lines(self,key,measures_per_line:int=2,measure_space= '  '):
        curr_measure_index = 0
        song_lines = []
        for _ in range(int(len(self.measure_list)/measures_per_line)):
            line_top = ''
            line_chords = ''
            for j in range(measures_per_line):
                curr_measure = self.measure_list[curr_measure_index]
                for mf in curr_measure.measure_fraction_list:
                    mf_line = mf.to_string(key)
                    mf_line_parts = mf_line.split('\n')
                    line_top =  f"{line_top}{mf_line_parts[0]}"
                    line_chords = f"{line_chords}{mf_line_parts[1]}"
                curr_measure_index +=1
                line_top = line_top + measure_space
                line_chords = line_chords + measure_space
            song_lines.append(line_top)
            song_lines.append(line_chords)
            
        measures_left = len(self.measure_list) % measures_per_line
        
        line_top = ''
        line_chords = ''
        for _ in range(measures_left):
            curr_measure = self.measure_list[curr_measure_index]
            for mf in curr_measure.measure_fraction_list:
                mf_line = mf.to_string(key)
                mf_line_parts = mf_line.split('\n')
#                 print(mf_line_parts)
                line_top =  f"{line_top}{mf_line_parts[0]}"
                line_chords = f"{line_chords}{mf_line_parts[1]}"
            curr_measure_index +=1
            line_top = line_top + measure_space
            line_chords = line_chords + measure_space
            
        song_lines.append(line_top)
        song_lines.append(line_chords)
        return song_lines
    
    def print_song(self,key,measures_per_line:int=2):
        song_lines = self.song_lines(key,measures_per_line)
        all_lines = '\n'.join(song_lines)
        line_length = len(song_lines[0])
        part_length= len(self.part_type)
        stars = '*' * int((line_length + part_length)/2)
        header = stars  + " " + self.part_type.upper() + " " + stars
        print(header)
        print(all_lines)
    
    def all_chords(self):
        r = []
        for m in self.measure_list:
            for mf in m.measure_fraction_list:
                r.append(mf.chord)
        return r
    
    def find_song_pattern(self,chord_pattern:list):
        ac = self.all_chords()
        plen = len(chord_pattern)
        ret = []
        for i in range(0,len(ac)-plen):
            # get chords from ac
            ac_i = ac[i:i+plen]
            ac_i_is_pattern = True
            for j in range(plen):
                if not ac_i[j]._issupersetof(chord_pattern[j]):
                    ac_i_is_pattern = False
                    
            if ac_i_is_pattern:
                ret.append(ac_i)
        return ret   
    
    def find_bass_pattern(self,bass_pattern:list):
        ac = self.all_chords()
        plen = len(bass_pattern)
        ret = []
        for i in range(0,len(ac)-plen):
            # get chords from ac
            ac_i = ac[i:i+plen]            
            ac_i_is_pattern = True
            for j in range(plen):
                bn = ac_i[j].chnum if ac_i[j].bass_num is None else ac_i[j].bass_num
                if bn != bass_pattern[j]:
                    ac_i_is_pattern = False
                    
            if ac_i_is_pattern:
                ret.append(ac_i)
        return ret   
    
class Song():
    def __init__(self,song_parts:list,title=None):
        self.song_parts = song_parts
        if type(self.song_parts)==np.ndarray:
            self.song_parts = self.song_parts.tolist()
        self.title = title
    def print_song(self,key):
        t = f"************************************* {self.title} *************************************"
        l = "-" * len(t)
        print(t)
        print(l)
        for i in range(len(self.song_parts)):
            sp = self.song_parts[i]
            sp.print_song(key)
            if i < len(self.song_parts)-1:
                print(" ")
    def all_chords(self):
        r = []
        for song in self.song_parts:
            r = r + song.all_chords()
        return r
    def find_song_pattern(self,chord_pattern):
        r = []
        for sp in self.song_parts:
            results = sp.find_song_pattern(chord_pattern)
            if len(results)>0:
                r.extend(results)
        return r

    def find_bass_pattern(self,bass_pattern):
        r = []
        for sp in self.song_parts:
            results = sp.find_bass_pattern(bass_pattern)
            if len(results)>0:
                r.extend(results)
        return r

    def name(self):
        ans = []
        frame = inspect.currentframe().f_back
        tmp = frame.f_globals 
        tmp.update(frame.f_locals)
        for k, var in tmp.items():
            if isinstance(var, self.__class__):
                if hash(self) == hash(var):
                    ans.append(k)
        return ans


# In[5]:


    


def diatonic_triad_chords():
    diatonic_triads = [Major,Minor,Minor,Major,Major,Minor]
    return [diatonic_triads[i](i+1) for i in range(len(diatonic_triads))]

def diatonic_chords():
    diatonic = [Major7,Minor7,Minor7,Major7,Dom7,Minor7,Minor7f5]
    return [diatonic[i](i+1) for i in range(len(diatonic))]

_diatonic_triads = diatonic_triad_chords()
_diatonic_chords = diatonic_chords()

class Diac1(Major7):
    def __init__(self):
        super(Diac1,self).__init__(1)
    

class Diac2(Minor7):
    def __init__(self):
        super(Diac2,self).__init__(2)

class Diac3(Minor7):
    def __init__(self):
        super(Diac3,self).__init__(3)

class Diac4(Major7):
    def __init__(self):
        super(Diac4,self).__init__(4)

class Diac5(Dom7):
    def __init__(self):
        super(Diac5,self).__init__(5)

class Diac6(Minor7):
    def __init__(self):
        super(Diac6,self).__init__(6)


class Diac7(Minor7f5):
    def __init__(self):
        super(Diac7,self).__init__(7)
        
class Diatr1(Major):
    def __init__(self):
        super(Diatr1,self).__init__(1)
    

class Diatr2(Minor):
    def __init__(self):
        super(Diatr2,self).__init__(2)

class Diatr3(Minor):
    def __init__(self):
        super(Diatr3,self).__init__(3)

class Diatr4(Major):
    def __init__(self):
        super(Diatr4,self).__init__(4)

class Diatr5(Major):
    def __init__(self):
        super(Diatr5,self).__init__(5)

class Diatr6(Minor):
    def __init__(self):
        super(Diatr6,self).__init__(6)


class Diatr7(Minorf5):
    def __init__(self):
        super(Diatr7,self).__init__(7)
        
        
                

def _make_measure(dfs_sp):
    if dfs_sp is None or len(dfs_sp)<1:
        return pd.DataFrame()
    pto = dfs_sp.iloc[0].part_type_ordered
    beats = dfs_sp.beats.sum()
    m = None
    try:
        m = Measure(dfs_sp.fraction.values,beats=beats)
    except Exception as e:
        print(e)
    return pd.DataFrame({'part_type_ordered':[pto],'measure':[m]})

def _make_songpart(dfm):
    if dfm is None or len(dfm)<1:
        return pd.DataFrame()
    pto = dfm.iloc[0].part_type_ordered
    sp = SongPart(dfm.measure.values,pto)
    return pd.DataFrame({'part_type_ordered':[pto],'song_part':[sp]})
    

def song_from_csv(df_song,title):
    dfs = df_song.copy()
    dfs.song_part2 = dfs.song_part2.fillna('')
#     dfs['part_type'] = dfs.apply(lambda r:r.song_part1 + ('' if len(r.song_part2) <1 else f"_{r.song_part2}"),axis=1) 
    dfs['part_type'] = dfs.song_part1 
    part_types = dfs.part_type.unique()
    part_types_ordered = [str(i) + "_" + part_types[i] for i in range(len(part_types))]
    df_pto = pd.DataFrame({'part_type':part_types,'part_type_ordered':part_types_ordered})
    dfs = dfs.merge(df_pto,on='part_type',how='inner')
    dfs = dfs.replace({np.nan: None})
    dfs['chnum'] = dfs.note
    dfs.majmin = dfs.majmin.apply(lambda v: DICT_MAJMIN[str(v).lower()])
    dfs.shfl = dfs.shfl.apply(lambda v: DICT_SHFL[str(v).lower()])
    dfs.bass_shfl = dfs.bass_shfl.apply(lambda v: DICT_SHFL[str(v).lower()])
    dfs.emb1_shfl = dfs.emb1_shfl.apply(lambda v: DICT_SHFL[str(v).lower()])
    dfs.emb2_shfl = dfs.emb2_shfl.apply(lambda v: DICT_SHFL[str(v).lower()])
    dfs['chord'] = dfs.apply(lambda r:Chord(
            int(r.chnum),
            shfl=r.shfl,
            majmin=r.majmin,
            emb1=None if r.emb1_num is None else Emb(int(r.emb1_num),r.emb1_shfl),
            emb2=None if r.emb2_num is None else Emb(int(r.emb2_num),r.emb2_shfl),
            bass_num = None if r.bass_num is None else int(r.bass_num),
            bass_shfl = r.bass_shfl
        ),axis=1)
    dfs['fraction'] = dfs.apply(lambda r:MeasureFraction(r.chord,num_32nds=r.beats),axis=1)
    dfs_fractions = dfs[['part_type_ordered','measure','fraction','beats']]
    dfs_measures = dfs_fractions.groupby(['part_type_ordered','measure'],as_index=False).apply(_make_measure)
    df_parts = dfs_measures.groupby('part_type_ordered',as_index=False).apply(_make_songpart)
    song = Song(df_parts.song_part.values,title)
    return song
    





