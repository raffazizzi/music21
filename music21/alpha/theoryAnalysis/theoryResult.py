# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         theoryResult.py
# Purpose:      Result objects to store information gathered about a score
#
# Authors:      Lars Johnson and Beth Hadley
#
# Copyright:    (c) 2009-2012 The music21 Project
# License:      LGPL or BSD, see license.txt
#-------------------------------------------------------------------------------

import music21
import unittest

class TheoryResult(object):
    '''
    A TheoryResult object is used to store information about the results
    of the theory analysis. Each object includes a direct references to the original segment
    in the score, in addition to a textual description of the result found, and a value. 
    Uses subclasses corresponding to the different types of objects
    '''
    _DOC_ATTR = {
    'text': '''The text associated with this theory result object, 
                    as generated by an identify() function''',
    'value': '''The value, typically a short string, associated with 
                    this theory result object, as generated by an identify() function''',
    'currentColor': 'The color of the entire theory result object',
    }
    def __init__(self):
        self.text = ""
        self.value = ""
        self.currentColor = ""
        
    def color(self,color):
        '''
        Bass-class method to color the individual elements in the theory result object.
        Polymorphically colors the theory result objects based on the type of object.
        '''
        self.currentColor = color

class VLQTheoryResult(TheoryResult):
    _DOC_ATTR = {
        'vlq': '''The actual :class:`~music21.voiceLeading.VoiceLeadingQuartet` 
                    object associated with this theory result object''',
        }
    def __init__(self, vlq):
        TheoryResult.__init__(self)
        self.vlq = vlq
        
    def color(self, color='red', noteList = (1, 2, 3, 4)):
        '''
        Color the notes in the vlq as specified by noteList, which is a list 
        of numbers 1-4 corresponding to the vlq map: 

        ::

            [ 1  2
              3  4  ] 

        Default is to color all notes
        '''
        self.currentColor = color
        if 1 in noteList:
            self.vlq.v1n1.color = color
        if 2 in noteList:
            self.vlq.v1n2.color = color
        if 3 in noteList:
            self.vlq.v2n1.color = color
        if 4 in noteList:
            self.vlq.v2n2.color = color
        
    def offset(self, leftAlign=False):
        '''
        returns the calculated offset of the vlq, which is just the maximum offset
        of all the notes inthe vlq
        
        if leftAlign=True, returns the minimum instead
        '''
        if leftAlign:
            return min(self.vlq.v1n1.offset, self.vlq.v2n1.offset, 
                        self.vlq.v1n2.offset, self.vlq.v2n2.offset)
        else:
            return max(self.vlq.v1n1.offset, self.vlq.v2n1.offset, 
                       self.vlq.v1n2.offset, self.vlq.v2n2.offset)

    def hasEditorial(self, miscKey, editorialValue=True):
        '''
        return True if any of the four VLQTheoryResult notes have the editorial key 
        .editorial.misc[miscKey] present and equal to a certain editorialValue (True by default)
        '''
        return ((miscKey in self.vlq.v1n1.editorial.misc and 
                    self.vlq.v1n1.editorial.misc[miscKey] == editorialValue) or 
                (miscKey in self.vlq.v1n2.editorial.misc and 
                    self.vlq.v1n2.editorial.misc[miscKey] == editorialValue) or 
                (miscKey in self.vlq.v2n1.editorial.misc and 
                    self.vlq.v2n1.editorial.misc[miscKey] == editorialValue) or 
                (miscKey in self.vlq.v2n2.editorial.misc and 
                    self.vlq.v2n2.editorial.misc[miscKey] == editorialValue))

    def markNoteEditorial(self, 
        editorialDictKey, 
        editorialValue,
        editorialMarkList=(1, 2, 3, 4)):
        '''
        Mark each note as specified in editorialMarkList with the 
        editorialValue in `Editorial.misc[editorialDictKey]`.
        
        `editorialMarkList` is a list with the notenumber in the 
        voiceleadingquartet to mark.

        ::

            [ 1  2
              3  4  ]

        Default is to mark all four notes with the editorial.
        '''

        if 1 in editorialMarkList:
            self.vlq.v1n1.editorial.misc[editorialDictKey] = editorialValue
        if 2 in editorialMarkList:
            self.vlq.v1n2.editorial.misc[editorialDictKey] = editorialValue
        if 3 in editorialMarkList:
            self.vlq.v2n1.editorial.misc[editorialDictKey] = editorialValue
        if 4 in editorialMarkList:
            self.vlq.v2n2.editorial.misc[editorialDictKey] = editorialValue
                  
class IntervalTheoryResult(TheoryResult):
    
    _DOC_ATTR = {'intv': '''The actual :class:`~music21.interval.Interval` 
                            object associated with this theory result object'''}
    
    def __init__(self, intv):
        TheoryResult.__init__(self)
        self.intv = intv
        
    def color(self, color='red', noteList=(1,2)):
        '''
        Color the notes in the interval as specified by noteList, 1 for the noteStart and 
        2 for the noteEnd
        default is to color all notes
        '''
        self.currentColor = color
        if 1 in noteList:
            self.intv.noteStart.color = color
        if 2 in noteList:
            self.intv.noteEnd.color = color
        
    def offset(self, leftAlign=False):
        '''
        returns the calculated offset of the vlq, which is just the largest offset
        between the first notes in both lines
        
        if leftAlign=True, returns the minimum instead
        '''
        if leftAlign:
            return min(self.intv.noteStart.offset, self.intv.noteEnd.offset) 
        else:
            return max(self.intv.noteStart.offset, self.intv.noteEnd.offset) 
        
    def lyric(self, value, noteList=(2,)):
        '''
        sets the lyric of the notes as specified by noteList, default is to only label 
        the noteEnd's lyric
        '''
        if 1 in noteList:
            self.intv.noteStart.lyric = value
        if 2 in noteList:
            self.intv.noteEnd.lyric = value
    
    def hasEditorial(self, miscKey, editorialValue=True):
        '''
        return True if either the noteStart or the noteEnd has the editorial key 
        .editorial.misc[miscKey] 
        present and equal to a certain editorialValue (True by default)
        '''
        return ((miscKey in self.intv.noteStart.editorial.misc and 
                    self.intv.noteStart.editorial.misc[miscKey] == editorialValue) or                 
                (miscKey in self.intv.noteEnd.editorial.misc and 
                 self.intv.noteEnd.editorial.misc[miscKey] == editorialValue))
    
# Note Theory Result Object
                  
class NoteTheoryResult(TheoryResult):
    
    _DOC_ATTR = {'n': '''The actual :class:`~music21.note.Note` 
                            object associated with this theory result object'''}
    
    def __init__(self, n):
        TheoryResult.__init__(self)
        self.n = n
        
    def color(self, color='red'):
        '''
        set the color of this note
        '''
        self.currentColor  = color
        self.n.color = color
            
class VerticalityTheoryResult(TheoryResult):     
    
    _DOC_ATTR = {'vs': '''The actual :class:`~music21.voiceLeading.Verticality`
                          object associated with this theory result object'''}  
         
    def __init__(self, vs): 
        TheoryResult.__init__(self)
        self.vs = vs
        
    def color(self, color ='red', partList=None):
        '''
        color all the notes from parts in partList. Default is to color all notes form all parts
        '''
        if partList:
            for partNum in partList:
                self.vs.noteFromPart(partNum).color = color
        else:
            for n in self.vs.noteList:
                n.color = color
                
            
class ThreeNoteLinearSegmentTheoryResult(TheoryResult): 
    
    _DOC_ATTR = {'tnls': '''The actual :class:`~music21.voiceLeading.ThreeNoteLinearSegment` 
                            object associated with this theory result object'''}          
          
    def __init__(self, tnls): 
        TheoryResult.__init__(self)
        self.tnls = tnls
        
    def color(self, color ='red', noteList=(2,)):
        '''
        color all the notes in noteList (1,2,3). Default is to color only the second note red
        '''
        if 1 in noteList:
            self.tnls.n1.color = color
        if 2 in noteList:
            self.tnls.n2.color = color
        if 3 in noteList:
            self.tnls.n3.color = color
        
class VerticalityNTupletTheoryResult(TheoryResult):
    
    _DOC_ATTR = {'vsnt': '''The actual :class:`~music21.voiceLeading.VerticalityNTuplet` 
                            object associated with this theory result object', 
                            'partNumIdentified':'Storate location for 
                            the part of importance that can be used later to color the results''' }     
    
    def __init__(self, vsnt, partNumIdentified=None): 
        TheoryResult.__init__(self)
        self.vsnt = vsnt #vertical slice ntuplet
        self.partNumIdentified = partNumIdentified
        
    def color(self,  color ='red', partNum=None, noteList=None):
        '''
        color the notes in partNum as specified by noteList (1,2,3, etc.)
        '''
        if noteList is None:
            noteList = []
        if partNum != None:
            print('color...', partNum, self.partNumIdentified, self.vsnt.nTupletNum, 
                  self.vsnt.tnlsDict.keys())
            if self.vsnt.nTupletNum == 3:                    
                self.vsnt.tnlsDict[partNum].color(color) 
        elif self.partNumIdentified !=None:
            if self.vsnt.nTupletNum == 3:
                self.vsnt.tnlsDict[self.partNumIdentified].color(color, [2] ) 

    def markNoteEditorial(self, editorialDictKey, editorialValue, editorialMarkDict=None):        
        '''
        editorialMarkDict is a dictionary denoting which object in the verticality Triplet to 
        mark with the editorial object. the keys of the dictionary correspond to which vertical
        slice (0, 1, 2, etc.) and the editorialValues are a list of the partNums to mark.
        
        Default editorialMarkDict = {2:[1]}
        '''
        if editorialMarkDict is None:
            editorialMarkDict = {2:[1]}
        for vsNum, partNumList in editorialMarkDict.items():
            for unused_counter_partNum in partNumList:
                self.vsnt.verticalities[vsNum].getObjectsByPart(0, 
                    classFilterList=['Note']).editorial.misc[editorialDictKey] = editorialValue


class Test(unittest.TestCase):
    
    def runTest(self):
        pass
        
class TestExternal(unittest.TestCase):
    
    def runTest(self):
        pass 
    
    def demo(self):
        pass

    
if __name__ == "__main__":

    music21.mainTest(Test)
    
    #te = TestExternal()
    #te.demo()
