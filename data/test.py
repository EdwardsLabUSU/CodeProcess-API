final_code ='''# CS 1XXX 
# Assignment 1 First Program
# Mr. Copy Paste

import random
randList = random.sample(range(0, 40), 10)
print("List")
print(randList)
print ("---Sorting List---")
# First Loop
for i in range(0, len(randList)):
    # Second Loop
    for j in range(0, len(randList)):
        if randList[i] > randList[j]:
            # Temp variable
            temp = randList[j]
            randList[j] = randList[i]
            randList[i] = temp
print("---Finished Sorting---")
print("List")
print(randList)

'''

snapShot = '''# CS 1XXX 
# Assignment 1 First Program
# Mr. Copy Paste

import random
randList = random.sample(range(0, 40), 10)
print("list")
print(randList)
print ("---Sorting List---")
for i in range(0, len(randList)):
    for j in range(0, len(randList)):
        if randList[i] > randList[j]:
            temp = randList[]
            randList[i] = randList[j]
            randList[j] = temp
print("finished sorting")
print("sorted list")
print(randList)

'''



def debug(s):
    #     print(s)
    ;
    class DiffHelper:
        def __init__(self, charjunk=None):
            self.charjunk = charjunk

        def _fancy_replace(self, abidx, a, alo, ahi, b, blo, bhi):
            r"""
        When replacing one block of lines with another, search the blocks
        for *similar* lines; the best-matching pair (if any) is used as a
        synch point, and intraline difference marking is done on the
        similar pair. Lots of work, but often worth it.
        Example:
        >>> d = Differ()
        >>> results = d._fancy_replace(['abcDefghiJkl\n'], 0, 1,
        ...                            ['abcdefGhijkl\n'], 0, 1)
        >>> print(''.join(results), end="")
        - abcDefghiJkl
        ?    ^  ^  ^
        + abcdefGhijkl
        ?    ^  ^  ^
        """

            # don't synch up unless the lines have a similarity score of at
            # least cutoff; best_ratio tracks the best score seen so far
            best_ratio, cutoff = 0.74, 0.75
            cruncher = difflib.SequenceMatcher(self.charjunk)
            eqi, eqj = None, None  # 1st indices of equal lines (if any)

            # search for the pair that matches best without being identical
            # (identical lines must be junk lines, & we don't want to synch up
            # on junk -- unless we have to)
            for j in range(blo, bhi):
                bj = b[j]
                cruncher.set_seq2(bj)
                for i in range(alo, ahi):
                    ai = a[i]
                    if ai == bj:
                        if eqi is None:
                            eqi, eqj = i, j
                        continue
                    cruncher.set_seq1(ai)
                    # computing similarity is expensive, so use the quick
                    # upper bounds first -- have seen this speed up messy
                    # compares by a factor of 3.
                    # note that ratio() is only expensive to compute the first
                    # time it's called on a sequence pair; the expensive part
                    # of the computation is cached by cruncher
                    if cruncher.real_quick_ratio() > best_ratio and \
                            cruncher.quick_ratio() > best_ratio and \
                            cruncher.ratio() > best_ratio:
                        best_ratio, best_i, best_j = cruncher.ratio(), i, j
            if best_ratio < cutoff:
                # no non-identical "pretty close" pair
                if eqi is None:
                    # no identical pair either -- treat it as a straight replace
                    # TODO fix this
                    #                 debug('here')
                    #                 yield None
                    abidx[0] += sum([len(a[ali]) for ali in range(alo, ahi)])
                    abidx[1] += sum([len(b[bli]) for bli in range(blo, bhi)])
                    #                 abidx[1] += bhi-blo
                    #                 debug(' '.join(['xx', str(ahi), str(alo), str(bhi), str(blo)]))
                    #                 yield from self._plain_replace(a, alo, ahi, b, blo, bhi)
                    return
                # no close pair, but an identical pair -- synch up on that
                best_i, best_j, best_ratio = eqi, eqj, 1.0
            else:
                # there's a close pair, so forget the identical pair (if any)
                eqi = None

            # a[best_i] very similar to b[best_j]; eqi is None iff they're not
            # identical

            # pump out diffs from before the synch point
            debug('yy')
            yield from self._fancy_helper(abidx, a, alo, best_i, b, blo, best_j)

            # do intraline marking on the synch pair
            aelt, belt = a[best_i], b[best_j]
            #         debug('synch pair:', aelt, belt)
            if eqi is None:
                # pump out a '-', '?', '+', '?' quad for the synched lines
                atags = btags = ""
                cruncher.set_seqs(aelt, belt)
                debug('zz')
                for tag, ai1, ai2, bj1, bj2 in cruncher.get_opcodes():
                    la, lb = ai2 - ai1, bj2 - bj1
                    #                 debug(' '.join(['zz', tag, a, b]))#a[abidx[0]], b[abidx[1]]]))
                    #                 debug(' '.join(['zz', tag, str(abidx[0]), str(abidx[1])]))
                    #                 print(abidx)
                    if tag == 'replace':
                        atags += '^' * la
                        btags += '^' * lb
                        abidx[0] += la
                        abidx[1] += la
                    elif tag == 'delete':
                        atags += '-' * la
                        abidx[0] += la
                    elif tag == 'insert':
                        btags += '+' * lb
                        abidx[1] += lb
                    elif tag == 'equal':
                        yield (abidx[0], abidx[1], la)
                        abidx[0] += la
                        abidx[1] += la
                        atags += ' ' * la
                        btags += ' ' * lb
                    else:
                        raise ValueError('unknown tag %r' % (tag,))
            #             yield from self._qformat(aelt, belt, atags, btags)
            else:
                # the synch pair is identical
                # TODO fix
                debug('ww')
                yield (abidx[0], abidx[1], len(aelt))
            #             yield '  ' + aelt

            # pump out diffs from after the synch point
            debug('gg')
            yield from self._fancy_helper(abidx, a, best_i + 1, ahi, b, best_j + 1, bhi)

        def _fancy_helper(self, abidx, a, alo, ahi, b, blo, bhi):
            g = []
            if alo < ahi:
                debug('hh')
                if blo < bhi:
                    #                 g = self._fancy_replace(abidx, a, alo, ahi, b, blo, bhi)
                    yield from self._fancy_replace(abidx, a, alo, ahi, b, blo, bhi)
                else:
                    debug('ii')
                    abidx[0] += ahi - alo
            #                 abidx[1] += bhi-blo
            #                 print('dump')
            #                 g = self._dump('-', a, alo, ahi)
            elif blo < bhi:
                debug('jj')
                #             abidx[0] += ahi-alo
                abidx[1] += bhi - blo

    #             print('dump')
    #             g = self._dump('+', b, blo, bhi)

    #         yield from g

    def test(linejunk, a, b):
        blocks = []
        cruncher = difflib.SequenceMatcher(linejunk, a, b)
        ai = 0
        bi = 0
        helper = DiffHelper()
        for tag, alo, ahi, blo, bhi in cruncher.get_opcodes():
            astr = ''.join(a[alo:ahi])
            bstr = ''.join(b[blo:bhi])
            #         print(tag, alo, ahi, blo, bhi, astr, bstr)
            print(tag, alo, ahi, blo, bhi)
            if tag == 'replace':
                yield from helper._fancy_replace([ai, bi], a, alo, ahi, b, blo, bhi)
                ai += len(astr)
                bi += len(bstr)
            #             g = self._fancy_replace(a, alo, ahi, b, blo, bhi)
            elif tag == 'delete':
                # in a
                ai += len(astr)
            #             g = self._dump('-', a, alo, ahi)
            elif tag == 'insert':
                # in b
                bi += len(bstr)
            #             g = self._dump('+', b, blo, bhi)
            elif tag == 'equal':
                #             blocks.append((ai, bi, len(astr)))
                block = (ai, bi, len(astr))
                ai += len(astr)
                bi += len(astr)
                yield block
            else:
                raise ValueError('unknown tag %r' % (tag,))

        return blocks

    blocks = test(None, final_code.splitlines(newline), snapShot.splitlines(newline))
    # for b in blocks:
    #     print(b)