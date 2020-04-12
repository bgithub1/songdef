'''
Created on Apr 10, 2020

@author: bperlman1
'''
import unittest
from songdef import songdef as sd
from _operator import indexOf

class Test(unittest.TestCase):
    
    def handle_double_shfl(self,note_string):
        ns = note_string
        fs = sd._FLAT+sd._SHARP
        sf = sd._SHARP+sd._FLAT
        ss  = sd._SHARP+sd._SHARP
        ff = sd._FLAT+sd._FLAT
        if fs in note_string:
            ns = note_string.replace(fs,'')
        elif sf in note_string:
            ns = note_string.replace(sf,'')
        elif ss in note_string:
            n = note_string[0]
            # move n to the next letter in the key of C
            cnotes = sd.KEYS['C']
            cindex = cnotes.index(n)
            new_cindex = 0 if cindex>=7 else cindex+1
            new_n = cnotes[new_cindex]
            ns = note_string.replace(n+ss,new_n)
        elif ff in note_string:
            n = note_string[0]
            # move n to the next letter in the key of C
            cnotes = sd.KEYS['C']
            cindex = cnotes.index(n)
            new_cindex = 7 if cindex<=0 else cindex-1
            new_n = cnotes[new_cindex]
            ns = note_string.replace(n+ff,new_n)
        return ns

    def assert_chords(self,chords,key,strings):
        for i in range(len(chords)):
            c = chords[i]
            s = strings[i]
            assert(c.to_string(key)==s)
            
    def chordtest(self,chords,shfl=None,keys_to_test=None):        
        strings_1 = ['','min','min','','','min','minf5']
        strings_2 = ['maj7','min7','min7','maj7','7','min7','min7f5']
        strings = strings_1 + strings_2
        
         
        if shfl is not None:
            ignore_note_index = [2,6,9,13] if shfl==sd.SharpFlat.SHRP else [0,3,7,10]
            for i in range(len(strings)):
                if i not in ignore_note_index:
                    strings[i] = str(shfl)+strings[i]
#         fs = sd._FLAT+sd._SHARP
#         sf = sd._SHARP+sd._FLAT
#         ss  = sd._SHARP+sd._SHARP
#         ff = sd._FLAT+sd._FLAT
        k2t = sd.KEYS.keys() if keys_to_test is None else keys_to_test
        for k in k2t:
            notes = sd.KEYS[k] * 2 
            results = [notes[i] + strings[i] for i in range(len(notes))]
            # get rid of 'f#', '#f','##' or 'ff'
            for i in range(len(results)):
                results[i] = self.handle_double_shfl(results[i])
#                 if fs in results[i]:
#                     results[i] = results[i].replace(fs,'')
#                 elif sf in results[i]:
#                     results[i] = results[i].replace(sf,'')
#                 elif ss in results[i]:
#                     n = results[i][0]
#                     # move n to the next letter in the key of C
#                     cnotes = sd.KEYS['C']
#                     cindex = cnotes.index(n)
#                     new_cindex = 0 if cindex>=7 else cindex+1
#                     new_n = cnotes[new_cindex]
#                     results[i] = results[i].replace(n+ss,new_n)
#                 elif ff in results[i]:
#                     n = results[i][0]
#                     # move n to the next letter in the key of C
#                     cnotes = sd.KEYS['C']
#                     cindex = cnotes.index(n)
#                     new_cindex = 7 if cindex<=0 else cindex-1
#                     new_n = cnotes[new_cindex]
#                     results[i] = results[i].replace(n+ff,new_n)
            self.assert_chords(chords,k,results)
    
    def testBf(self):
        c = sd.Major(4)
        print(c.to_string('F'))
    
            
    def test1DiaChord(self):
        chords_1 = [sd.Diatr1(),sd.Diatr2(),sd.Diatr3(),sd.Diatr4(),sd.Diatr5(),sd.Diatr6(),sd.Diatr7()]
        chords_2 = [sd.Diac1(),sd.Diac2(),sd.Diac3(),sd.Diac4(),sd.Diac5(),sd.Diac6(),sd.Diac7()]
        chords = chords_1 + chords_2
        self.chordtest(chords)
        
    def test2MajorMinorChord(self):
        chords_1 = [sd.Major(1),sd.Minor(2),sd.Minor(3),sd.Major(4),sd.Major(5),sd.Minor(6),sd.Minorf5(7)]
        chords_2 = [sd.Major7(1),sd.Minor7(2),sd.Minor7(3),sd.Major7(4),sd.Dom7(5),sd.Minor7(6),sd.Minor7f5(7)]
        chords = chords_1 + chords_2
        self.chordtest(chords)
    
    def test21Csharpsharp(self):
        c = sd.Minor7(2,shfl=sd.SharpFlat.SHRP)
        cs = c.to_string('B')
        assert(cs=='Dmin7')
        
    def test3Bsharp(self):
        chords_1 = [sd.Major(1),sd.Minor(2),sd.Minor(3),sd.Major(4),sd.Major(5),sd.Minor(6),sd.Minorf5(7)]
        chords_2 = [sd.Major7(1),sd.Minor7(2),sd.Minor7(3),sd.Major7(4),sd.Dom7(5),sd.Minor7(6),sd.Minor7f5(7)]
        chords = chords_1 + chords_2
        shfl  = sd.SharpFlat.SHRP
        for i in range(len(chords)):
            if i not in [2,6,9,13]:
                chords[i].shfl = shfl
        self.chordtest(chords,shfl,keys_to_test=['B'])

    def test4AllSharps(self):
        chords_1 = [sd.Major(1),sd.Minor(2),sd.Minor(3),sd.Major(4),sd.Major(5),sd.Minor(6),sd.Minorf5(7)]
        chords_2 = [sd.Major7(1),sd.Minor7(2),sd.Minor7(3),sd.Major7(4),sd.Dom7(5),sd.Minor7(6),sd.Minor7f5(7)]
        chords = chords_1 + chords_2
        shfl  = sd.SharpFlat.SHRP
        for i in range(len(chords)):
            if i not in [2,6,9,13]:
                chords[i].shfl = shfl
        self.chordtest(chords,shfl)

       
    def dtest5SpecificChords(self):
        k = 'D'
        onech =sd.Major(1)
        fourchmaj7 = sd.Major7(4)
        twomin7 = sd.Chord(2,majmin=sd.MajMin.MIN,emb1=7)
        threemin7 = sd.Chord(3,majmin=sd.MajMin.MIN,emb1=7)
        sixmin7 = sd.Minor7(6)
        threeflatmin7 = sd.Chord(3,shfl=sd.SharpFlat.FLAT,majmin=sd.MajMin.MIN,emb1=7)
        sevenminor7f5 = sd.Minor7f5(7)
        assert(twomin7.to_string(k)=='Emin7')
        assert(threemin7.to_string(k)=='F#min7')
        assert(onech.to_string(k)=='D')
        assert(fourchmaj7.to_string(k)=='Gmaj7')
        assert(sixmin7.to_string(k)=='Bmin7')
        assert(sevenminor7f5.to_string(k)=='C#min7f5')
        
        m1=sd.Major7(4)
        m2=sd.Major7(3)
        m3=sd.Major7(4)
    
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
        
        m4 = sd.Minor7(7)
        m5 = sd.Minor7f5(7)
        assert(m5>m4)
            
    def dtest6Emb(self):
        e1 = sd.Emb(5,shfl=sd.SharpFlat.SHRP)
        e2 = sd.Emb(5)
        assert(e1>=e2)
        assert(not e1<=e2)
        assert(e1>e2)
        assert(not e1<e2)
    
        assert(not e2>=e1)
        assert(e2<=e1)
        assert(not e2>e1)
        assert(e2<e1)
    
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    