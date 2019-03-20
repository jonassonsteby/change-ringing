Find change ringing sequences with cr.py
========================================

#### Features

- Find all change ringing sequences of all lengths for 1,2,3 and 4 bells.
- Find some of the sequences for 5,6,7,8 and 9 bells. For a given number of
  bells, the `findAll` method starts with finding all sequences of length 1,
  then moves on to sequences of length 2 and so on. The sequences of length L
  is used to find the sequences of length L+1.
- Categorize sequences into separate files by number of bells (n), sequence
  length (L) and sequence type.
- Choose any starting permutation. Use any string of n unique characters. 1
  char = 1 bell. If there are more than one of any of the characters, you will
  get faulty results.

#### Limitations

- Prone to gobble up memory when n > 4. You should therefore be conservative
  with the sequence length (L) when n > 4. On my 8 GB RAM laptop I observed the
  memory starting to take off around
 - L=11 for n=5
 - L=7  for n=6
 - L=6  for n=7
 - L=6  for n=8
 - L=5  for n=9

   Monitor your memory and kill the script before your computer starts
   swapping. Patterns are written to file for each completed L, hence you will
   only loose the sequences found for the current L.
- Initial setup starts to slow down at n=8 (without spiking memory).

Usage
-----

Running

    $ python cr.py

will find all cyclic sequences for n=4 and write them to file. Edit `cr.py` if
you want to find other sequences. Make sure that you have initiated a
`ChangeRinging` object before you call any methods. E.g.

    c = ChangeRinging('1234')

which sets your starting permutation to '1234' (n=4) and labels the bells
'1','2','3' and '4'. Then you can call e.g.

    c.findAll(option=1)

to find all path sequences. The `findAll` method takes 3 optional arguments.

    findAll(L=<int>,filename=<str>,option=<int>)

where

- `L` is the maximum length of the sequences you want to find. `L` must be an
  integer in [1,factorial(n)]. The default is factorial(n) which is the longest
  possible sequence for n bells.
- `filename` sets custom filename. The sequence length will be appended before
  the extension. The default is `change<n>-<sequence type><L>.txt`.
- __`option`__
  - Set `option=0` to find cyclic sequences. [Default]
  - Set `option=1` to find path sequences.
  - Set `option=2` to find noncappable sequences.


Find change ringing transition rules with tr.py
===============================================
Run

    $ python tr.py

to find the allowable transition rules for n=1,..,26 bells. You can find more
if you'd like. The rules will be decorated with a symbol ('><') to indicate
the swapping of two bells and written to separate files for each n.

`tr.py` utilizes the ChangeRinging module from `cr.py`, so you need to run in
from a directory also containing `cr.py`.

If you are only looking for the _number of_ allowable transition rules, then you
should rather take a look at [http://oeis.org/A000071](http://oeis.org/A000071) (__spoiler alert!__).


What is change ringing?
=======================

Examples of change ringing sequences for 3,4 and 5 bells respectively.

            123    1234    12345
            132    1243    12354
            312    2134    13245
            321    2143    13254
            231    2413    31245
            213    2431    31254
            123    4213    32145
                   4231    32154
                   4321    23154
                   4312    21354
                   4132    12345
                   4123
                   1423
                   1432
                   1342
                   3124
                   3214
                   2314
                   2341
                   3241
                   3421
                   3412
                   3142
                   1324
                   1234


Change ringing is a very specific way of making music with an arbitrary
(natural) number of uniquely pitched bells (labeled with the numbers 1,2,...,n
in descending order of pitch). The bells are rung only one at the time in rapid
succession with regular time intervals. No bell is allowed to ring again before
all bells have been rung. Thus a piece of this music consists of a sequence of
what is called _changes_, _rows_ or _permutations_, that is, the act of ringing
through all the n bells once in some order. All permutations are allowed, but
not all sequences of permutations are allowed. For starters, you cannot repeat
a previously rung permutation within a sequence, which gives these sequences a
maximum length of factorial(n). Still, most of the sequences satisfying this
criterion are not allowed due to several more criteria. Let us take a look at a
complete definition to see exactly what types of sequences of permutations that
are allowed in change ringing.

Let n be a positive integer. A ___change ringing sequence for n bells___ is a
sequence of permutations of the set {1,2,...,n} that satisfies the following
criteria.

1. The position of each bell (number) from one permutation to the next can stay
   the same or move by at most one place.
2. No permutation can be repeated except for the starting permutation which can
   be repeated at most once at the end of the sequence to accommodate criterion
   4.
3. The sequence must start with the permutation (1,2,...,n)

  Optional criteria that differentiates types of sequences.

4. The sequence must end with the same permutation that it started with.
5. The sequence must contain all permutations.

There exists a few more optional criteria
([look here](https://math.ch/TMU2017/Campanology_Ringing_the_changes.pdf)),
but they are not relevant for this project. Also, sometimes criterion 3 is
viewed as optional instead of mandatory.

My own definitions for use in this project
------------------------------------------

We define the ___length___ of a change ringing sequence as the number of unique
permutations in the sequence.

We define a ___cyclic sequence___ as a sequence that satisfies criterion
1,2,3,4. These sequences start and end with (1,2,...,n).

We define a ___path sequence___ as a sequence that satisfies criterion 1,2,3
and __not__ 4.

We define a ___noncappable sequence___ as a path sequence that has an ending
permutation that cannot immeadiately transition to the starting permutation.
Thus we cannot append the starting permutation (cap it and make it cyclic)
without breaking criterion 1.

Transitions
-----------

Criterion 1 heavily limits the number of ___allowable transitions___  (also
called ___allowable transition rules___) from one permutation to another .

For n=2 there is only 1 allowable transition.

        ab
        ><
        ba

For n=3 there are 2 allowable transitions.

        abc   abc
        ><     ><
        bac   acb

For n=4 there are 4.

        abcd    abcd    abcd    abcd
        ><       ><       ><    ><><
        bacd    acbd    abdc    badc

There are 24 permutations of four bells, thus most permutations are out of
reach in a single transition. This continues to be the case for larger numbers
of bells, as the ratio of number of allowable transition rules to the number of
permutations tends to zero as n tends to infinity
((n+1)-th element of [A000071](http://oeis.org/A000071) divided by factorial(n)).


Resources
=========

[Video (6:28) from Simons Foundation](https://www.youtube.com/watch?v=3lyDCUKsWZs)

[Fabia Weber's bachelor thesis: Campanology - Ringing the changes](https://math.ch/TMU2017/Campanology_Ringing_the_changes.pdf)

