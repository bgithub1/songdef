#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from enum import Enum
import copy
import pdb


_SHARP = '#'
_FLAT = 'f'
_PLUS = '+'
_FSP = [_FLAT,_SHARP,_PLUS]

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
    i = key_array.index_of(note) + up_down
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
        
        
class Chord():
    def __init__(self,
                 chnum: int,
                 shfl: SharpFlat=None,
                 majmin: MajMin=None,
                 emb1: Emb=None,
                 emb2: Emb=None,
                 bass_num: int=None,
                 bass_shfl: SharpFlat=None,
                 key=None):
        self.chnum = chnum
        self.shfl = shfl
        self.majmin = majmin
        self.emb1 = emb1
        self.emb2 = emb2
        self.bass_note = None
        self.bass_num = bass_num
        self.bass_note = str(self.bass_num)
        self.bass_shfl = bass_shfl
        self.key = self.change_key(key)

    def change_key(self,key):
        self.chnote = None
        self.key = key
        if key is not None :
            key2 = key[0].upper() 
            if len(key)>1:
                # there may be a sharp or flat
                key2 = key2 + key[1]
                self.key = key2 # format key string properly, with first char capital
            key_array = KEYS[self.key]
            self.chnote = key_array[self.chnum-1]
        if self.bass_num is not None:
            if key is not None :
                self.bass_note = key_array[self.bass_num-1]
            else:
                self.bass_note = str(self.bass_num)
        else:
            self.bass_note = None
            
    def __str__(self):
        bass_note = self.bass_note
        bass_note = '/' + str(bass_note) if bass_note is not None else ''
        bass_shfl = self.bass_shfl if self.bass_shfl is not None else ''
        bn = bass_note + bass_shfl
        bn = bn.strip()
        emb1 = str(self.emb1) if self.emb1 is not None else ''
        emb2 = str(self.emb2) if self.emb2 is not None else ''
        chn = self.chnum if self.chnote is None else self.chnote
        mn = str(self.majmin) if self.majmin is not None else ''
        mn = mn.lower()
        # handle sharp flat
        shfl = ''
        if self.shfl is not None:
            if str(chn) in '1234567':
                chn = str(chn) + str(self.shfl)
            else:
                if self.shfl == SharpFlat.FLAT:
                    if _SHARP in str(chn):
                        chn = chn.replace(_SHARP,'')
                    elif _FLAT in str(chn):
                        chn = next_note(self.key,chn,up_down=-1)
                        
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


# In[3]:


def test_emb():
    e1 = Emb(5,shfl=SharpFlat.SHRP)
    e2 = Emb(5)
    assert(e1>=e2)
    assert(not e1<=e2)
    assert(e1>e2)
    assert(not e1<e2)

    assert(not e2>=e1)
    assert(e2<=e1)
    assert(not e2>e1)
    assert(e2<e1)


# In[4]:


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
        chord.change_key(key)
        
        l = "_" * self.num_32nds
        c = str(chord).replace(' ','')
        c = c + " " * (len(l) - len(c))
        c = c[0:len(l)]
        return f"{l}\n{c}"
        
class Measure():
    def __init__(self,measure_fraction_list: list=None):
        # what kind of obect is measure_fraction_list
        self.measure_fraction_list = []
        if type(measure_fraction_list) == list:
            for mf in measure_fraction_list:
                self.add_fraction(mf)
        else:
            # measure_fraction_list is a tuple, MeasureFraction instance, or a Chord
            self.add_fraction(measure_fraction_list)
            
    def add_fraction(self,mf):
            if (type(mf) == MeasureFraction) or (issubclass(type(mf),MeasureFraction)):
                self.measure_fraction_list.append(mf)
            elif type(mf)==tuple:
                # it's a tuple
                self.measure_fraction_list.append(MeasureFraction(mf[0],mf[1] if len(mf)>1 else 32))
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
    
class Song():
    def __init__(self,song_parts:list):
        self.song_parts = song_parts
    def print_song(self,key):
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


# In[5]:


def test_chords():
    onech = Major(1,key='D')
    fourchmaj7 = Major7(4,key='D')
    twomin7 = Chord(2,majmin=MajMin.MIN,emb1=7,key='D')
    threemin7 = Chord(3,majmin=MajMin.MIN,emb1=7,key='D')
    sixmin7 = Minor7(6,key='D')
    threeflatmin7 = Chord(3,shfl=SharpFlat.FLAT,majmin=MajMin.MIN,emb1=7,key='D')
    sevenminor7f5 = Minor7f5(7,key='D')
    assert(str(twomin7)=='Emin7')
    assert(str(threemin7)=='F#min7')
    assert(str(onech)=='D')
    assert(str(fourchmaj7)=='Gmaj7')
    assert(str(sixmin7)=='Bmin7')
    assert(str(sevenminor7f5)=='C#min7f5')
    
    m1=Major7(4,key='D')
    m2=Major7(3,key='D')
    m3=Major7(4,key='D')

    assert(m1.__gt__(m2))
    assert(m1.__ge__(m2))
    assert(not m2.__gt__(m1))

    assert(m2.__lt__(m1))
    assert(m2.__le__(m1))
    assert(not m1.__lt__(m2))

    assert(m1.__ge__(m3))
    assert(m1.__le__(m3))
    assert(not m1.__lt__(m3))
    assert(m3.__ge__(m1))
    assert(m3.__le__(m1))
    assert(not m3.__lt__(m1))
    assert(m3.__eq__(m1))
    
    m4 = Minor7(7,key='C')
    m5 = Minor7f5(7,key='C')
    assert(m5>m4)
    


def diatonic_triad_chords():
    diatonic_triads = [Major,Minor,Minor,Major,Major,Minor]
    return [diatonic_triads[i](i+1,key='Ef') for i in range(len(diatonic_triads))]

def diatonic_chords():
    diatonic = [Major7,Minor7,Minor7,Major7,Dom7,Minor7,Minor7f5]
    return [diatonic[i](i+1,key='E') for i in range(len(diatonic))]

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
        
        
                






