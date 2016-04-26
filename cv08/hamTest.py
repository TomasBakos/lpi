#! /bin/env python3
#
# Testovaci program pre ham kniznicu
#
# Kniznica musi byt v subore ham.py a musi implementovat triedu
# HamiltonianCycle s metodou find.
#

import sys
import time
import traceback
import random
import itertools

from ham import HamiltonianCycle

""" Nastavte na True ak chcete aby testy zastali na prvej chybe. """
stopOnError = False

class FailedTestException(BaseException):
    pass

def now():
    try:
       return time.perf_counter() # >=3.3
    except AttributeError:
       return time.time() # this is not monotonic!

def printException():
    print('ERROR: Exception raised:\n%s\n%s\n%s' % (
        '-'*20,
        traceback.format_exc(),
        '-'*20)
    )

class Tester(object):
    def __init__(self):
        self.case = 0
        self.tested = 0
        self.passed = 0

    def fail(self, msg):
        print('ERROR: %s' % msg)
        return False;

    def checkGood(self, m, r):
        if len(m) != len(r):
            return self.fail('Wrong result length!')
        last = r[-1]
        for v in r:
            if not m[last][v]:
                return self.fail('No edge %d -> %d' % (last, v))
            last = v
        return True

    def checkBad(self, r):
        if len(r) != 0:
            return self.fail('non-empty result when there should be no cycle')
        return True

    def check(self, m, good, r):
        if good:
            return self.checkGood(m, r)
        else:
            return self.checkBad(r)


    def test(self, m, good):
        self.case += 1
        self.tested += 1
        sys.stdout.write('Case %d:  ' % (self.case,))

        try:
            rs = random.getstate()
            start = now()
            r = HamiltonianCycle().find(m)
            duration = now() - start
            random.setstate(rs)
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            printException()
            if stopOnError:
                raise FailedTestException()
            return


        if self.check(m, good, r):
            self.passed += 1
            print('PASSED  duration %s' % duration)
        else:
            print('edges:')
            for row in m:
                print(' '.join(('1' if x else '0') for x in row))
            print('')
            print('result: %s' % repr(r))
            print('')
            if stopOnError:
                raise FailedTestException()

    def status(self):
        print("self.tested %d" % (self.tested,))
        print("self.passed %d" % (self.passed,))
        if self.tested == self.passed:
            print("OK")
        else:
            print("ERROR")


def edgesToIncidenceMatrix(edges):
    a, b = zip(*edges)
    n = max(a+b)+1

    m = []
    for row in range(n):
        m.append([False] * n)
    for a,b in edges:
        m[a][b] = True
    return m


def randomGoodInput(size):
    maxv = size-1
    m = edgesToIncidenceMatrix([(maxv, maxv)])
    for r in range(size):
        for c in range(size):
                m[r][c] = random.randint(0,1) == 1

    sol = list(range(size))
    random.shuffle(sol)
    last = sol[-1]
    for v in sol:
        m[last][v] = True
        last = v
    return m


def randomBadInput(size):
    def goodPath(m, path):
        last = path[-1]
        for v in path:
            if not m[last][v]:
                return False
            last = v
        return True

#    print('Generating BAD input of size %d' % size)
    m = []
    for r in range(size):
        m.append([True]*size)

    for perm in itertools.permutations(range(size)):
        if goodPath(m, perm):
            i = random.randrange(len(perm))
            j = (i+1)%len(perm)
            m[perm[i]][perm[j]] = False
#    print('Done generating')
#    print(repr(m))
    return m

random.seed(47)

t = Tester()
try:

    m = [
            [True, True],
            [True, True]
        ]
    t.test(m, True)

    m = [
            [False, True],
            [False, False],
        ]
    t.test(m, False)

    m = edgesToIncidenceMatrix([
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 3),
            (1, 4),
            (2, 1),
            (2, 5),
            (3, 0),
            (3, 4),
            (4, 1),
            (4, 2),
            (4, 5),
            (5, 2),
            (5, 4),
        ])

    t.test(m, True)

    t.test(randomGoodInput(10), True)

    t.test(randomGoodInput(20), True)

    t.test(randomGoodInput(50), True)

    t.test(randomBadInput(5), False)

    t.test(randomBadInput(10), False)

    m = [
        [True, True, True, True, True, False, False, True, True, True, True, False, True, False, False],
        [False, True, False, False, False, True, False, False, True, True, True, True, False, True, True],
        [False, False, True, False, False, False, False, False, True, False, True, False, True, False, False],
        [False, False, False, True, False, True, False, False, True, False, True, False, True, False, True],
        [False, False, False, False, True, True, False, False, False, False, True, True, True, True, True],
        [False, False, False, False, False, True, False, False, True, False, True, True, True, True, True],
        [False, False, False, False, False, False, True, False, True, True, True, True, True, True, True],
        [False, False, False, False, False, False, False, True, False, True, True, True, True, True, True],
        [False, False, False, False, False, False, False, False, True, False, True, False, False, True, True],
        [False, False, False, False, True, True, False, True, False, True, True, True, True, True, True],
        [False, False, True, True, True, True, False, False, False, True, True, True, True, True, False],
        [False, False, True, False, False, True, False, True, True, True, False, True, False, False, False],
        [False, False, True, True, True, True, False, True, True, True, False, False, True, False, False],
        [True, False, True, True, True, True, True, True, True, True, False, False, False, True, False],
        [False, True, True, True, False, True, False, False, True, False, False, False, False, False, True]
    ]
    t.test(m, False)

    print("END")

except FailedTestException:
    print("Stopped on first failed test!")
finally:
    t.status()

# vim: set sw=4 ts=4 sts=4 et :
