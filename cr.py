# coding=utf-8
import time
from math import factorial
import sys

def timeStr(t):
    secs = t%60
    t = t//60
    mins = t%60
    t = t//60
    hours = t%24
    days = t//24
    d = ' '
    h = ' '
    m = ' '
    s = ' '
    if days >= 2:  d = 's'
    if hours >= 2: h = 's'
    if mins >= 2:  m = 's'
    if secs >= 2:  s = 's'
    D = '%3d day%s' % (days,d)
    H = '%2d hour%s' % (hours,h)
    M = '%2d min%s' % (mins,m)
    S = '%5.2f sec%s' % (secs,s)
    return '%s %s %s %s' % (D,H,M,S)

class Timer:

    def __init__(self,label='Time'):
        self.label = label
        self.t0 = None
        self.t1 = None

    def start(self):
        if self.t0 == None:
            self.t0 = time.process_time()

    def stop(self):
        if not (self.t0 == None):
            self.t1 = time.process_time()
            border = 60*'='
            tdiff = self.t1-self.t0
            print(border+'\n%s:' % self.label +timeStr(tdiff)+'\n'+border)
            self.t0 = None
            self.t1 = None
            return tdiff

def permutations(s):
    """Find the permutations of the character order of a string"""
    p = []
    if len(s) > 1:
        e = s[0]
        r = s[1:]
        var = permutations(r)
        for i in range(len(var)):
            for j in range(len(var[i])):
                p.append(var[i][0:j]+e+var[i][j:])
            p.append(var[i]+e)
        return p
    else:
        return [s]

class ChangeRinging:

    def __init__(self,startingPermutation, setup=True):
        self.startingPermutation = startingPermutation
        self.n = len(startingPermutation) # Number of bells
        self.transList = self.transitions(self.n) # List of transition rules
        self.NoTR = len(self.transList) # Number of Transition Rules
        self.maxL = factorial(self.n) # Max length of change ringing sequence for this n
        self.OAI = self.maxL - self.NoTR - 1 # One Away Index
        self.t0 = None
        self.t1 = None
        self.toStr = {}
        self.toNum = {}
        self.rule = []

        # Initiate setup for finding change ringing patterns.
        #  The setup is slow for n > 8. You can bypass the setup by
        #  instanciating the class with setup=False
        if setup: self.setup()

    def setup(self):
        """Setup for finding change ringing patterns"""

        timer = Timer('Setup time')
        timer.start()

        permList = permutations(self.startingPermutation)

        # Move the permutations that can immeadiately transition to the starting
        # permutation at the very end such that we can easier test whether some
        # permutation is one of these (last permutation in a cyclic sequence must
        # be). Below we will alias our permutations as integers such that we
        # can (amongst other things) test it by
        #                 if somePermutation > self.OAI:
        for i in range(self.NoTR):
            perm = self.transition(i,permList[0])
            permList.remove(perm)
            permList.append(perm)

        # alias permutations as integers [0,factorial(n)-1]
        for i in range(len(permList)):
            self.toStr[i]=permList[i]
            self.toNum[permList[i]] = i

        # transition rules for permutations in aliased form
        for i in range(self.NoTR):
            self.rule.append([0 for j in range(self.maxL)])

        for i in range(self.NoTR):
            for j in range(self.maxL):
                self.rule[i][j] = self.toNum[self.transition(i,self.toStr[j])]

        timer.stop()

    def transitions(self,n):
        """Finds the transitions rules for n bells"""
        if n < 2:
            return []
        if n == 2:
            return [[1,0]]
        else:
            prev = self.transitions(n-1)
            for change in prev:
                change.append(n-1)
            temp = prev.copy()
            temp.append([i for i in range(n)])
            add = []
            for i in range(len(temp)):
                if (temp[i][-2]==n-2):
                    new = temp[i][:-2] + [temp[i][-1]] + [temp[i][-2]]
                    add.append(new)
            return prev + add

    def transition(self,cNr,s):
        """Changes a string with transition nr cNr where 0 <= cNr <= NoTR """
        p = list(s)
        changed = p.copy()
        for i in range(self.n):
            changed[i] = p[self.transList[cNr][i]]
        return "".join(changed)

    def find(self,L):
        """Find path sequences of length L"""
        if L == 0:
            return []
        elif L == 1:
            return [[0]]
        else:
            sequences = []
            prev_sequences = self.find(L-1)
            for i in range(len(prev_sequences)):
                S = prev_sequences[i]
                for j in range(self.NoTR):
                    new = self.rule[j][S[-1]]
                    if not (new in S):
                        sequences.append(S+[new])
            return sequences

    def removeNoncappable(self,path):
        cyclic = []
        for S in path:
            if S[-1] > self.OAI:
                cyclic.append(S)
        return cyclic


    def removeCappable(self,path):
        noncappable = []
        for S in path:
            if S[-1] <= self.OAI:
                noncappable.append(S)
        return noncappable

    def process(self,sequences,option):
        if option == 0:
            processed_sequences = self.removeNoncappable(sequences)
        elif option == 1:
            processed_sequences = sequences
        elif option == 2:
            processed_sequences = self.removeCappable(sequences)
        else:
            raise ValueError("'option' must be an integer either 0,1 or 2")
        return processed_sequences

    def opt2str(self,option):
        if option == 0:
            return 'c'
        elif option == 1:
            return 'p'
        elif option == 2:
            return 'x'
        else:
            raise ValueError("'option' must be an integer either 0,1 or 2")

    def addNumbering(self,L,filename=None,option=0):
        if filename == None:
            # default filename
            filename = 'change%d-%s%d.txt' % (self.n,self.opt2str(option),L)
        else:
            lnr = '-%d.' % L
            strs = filename.split('.')
            filename = strs[0] + lnr + strs[1]
        return filename

    def writeToFile(self,L,sequences,filename=None,option=0):
        endOfSeq = '\n'
        if option == 0:
            # cap the cappables to make them cyclic
            endOfSeq = self.toStr[0]+'\n\n'
        if L == 1:
            if option == 2: sequences = []
            else: endOfSeq = '\n'
        count = len(sequences)
        f = open(filename,'w')
        f.write('Number of sequences = ' + str(count) + '\n\n')
        for S in sequences:
            for nr in S:
                f.write(self.toStr[nr]+'\n')
            f.write(endOfSeq)
        f.close()
        print('L=%2d, found %d' % (L,count))

    def findOne(self,L=9,filename=None,option=0):
        print('Searching for L=%d ...' % L)
        sequences = self.process(self.find(L),option)
        if L == 1 and option == 0: sequences = [[0]]
        self.writeToFile(L,sequences,self.addNumbering(L,filename,option),option)
        return sequences

    def findAll(self,L=None,filename=None,option=0):
        """Modified find(self,L)"""
        if L == None: L = self.maxL
        if L == 0:
            self.writeToFile(L,[],self.addNumbering(L,filename,option),option)
            return []
        elif L == 1:
            self.writeToFile(L,[[0]],self.addNumbering(L,filename,option),option)
            return [[0]]
        else:
            sequences = []
            prev_sequences = self.findAll(L-1,filename,option)
            for i in range(len(prev_sequences)):
                S = prev_sequences[i]
                for j in range(self.NoTR):
                    new = self.rule[j][S[-1]]
                    if not (new in S):
                        sequences.append(S+[new])

            # process and write to file
            processed_sequences = self.process(sequences,option)
            self.writeToFile(
                              L
                             ,processed_sequences
                             ,self.addNumbering(L,filename,option)
                             ,option
                            )

            return sequences

if __name__ == "__main__":

    # Choose starting permutation (max n=9!)
    c = ChangeRinging('1234')

    timer = Timer('Searching time')
    timer.start()

    c.findAll() # find all cyclic sequences

    timer.stop()


    ##### Examples #####

    ## Use the option variable to choose type of sequence
    ##    option = 0 :: cyclic sequences      (c)
    ##    option = 1 :: path sequences        (p)
    ##    option = 2 :: noncappable sequences (x)

    ## custom filename
    #c.findAll(filename='cyclic_change_n.txt')

    ## find up to and including length 10
    #c.findAll(L=10)

    ## find all path sequences
    #c.findAll(filename='path_change_n.txt',option=1)

    ## find all noncappable sequences
    #c.findAll(filename='noncappable_change_n.txt',option=2)

    ## find one specific sequence
    #c.findOne(L=11,filename='sequence.txt',option=0)

