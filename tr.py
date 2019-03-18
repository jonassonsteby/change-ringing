from cr import ChangeRinging

def findTransitions(n):
    """
    Find all of the transition rules for n bells and write these to a file.
    """
    bellSymbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    syms = bellSymbols[:n]
    f = open('transitions%d.txt' % n,'w')
    c = ChangeRinging(syms, setup=False)
    transList = c.transList
    f.write('n=%d\ncount = %d' % (n,c.NoTR))
    for i in range(c.NoTR):
        newChange = c.transition(i,syms)
        s = ''
        for j in range(n):
            if syms[j] > newChange[j]:
                s += '<'
            elif syms[j] < newChange[j]:
                s += '>'
            else:
                s += ' '
        f.write('\n\n' + syms + '\n' + s + '\n' + newChange)
    print('n=%2d, found %d' % (n,c.NoTR))
    f.close()

if __name__ == "__main__":
    # find transitions rules for n=1,...,26
    for i in range(26):
        findTransitions(i+1)
