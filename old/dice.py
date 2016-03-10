from itertools import product

class Dice:        
    def __init__(self, maxv):
        min_chance = 0.5 / 100
        self.maxexp = min(x for x in range(1,10) if min_chance*maxv**x >= 1)
        self.maxv = maxv
        self.vals = [0]
        self.freq = self.calcFreq()
        self.vals_n = [x for x in self.vals if x != 0]
    
    def calcFreq(self):
        max_on_step = 1.0
        prev_max = 1
        cur_max = self.maxv
        r = {}
        calculated_freq = 0.0
        
        for i in range(self.maxexp):
            self.vals += range(prev_max, cur_max)

            cur_index = [x for x in range(prev_max, cur_max)]
            cur_frequency = max_on_step/self.maxv
            r[tuple(cur_index)] = cur_frequency
            
            calculated_freq += (cur_frequency)*(len(cur_index))
            
            max_on_step = cur_frequency
            prev_max = cur_max+1
            cur_max += self.maxv
            
        r[(0,)] = 1.0 - calculated_freq
        return r

    def getFreq(self):
        r = ''
        for j in sorted(self.freq):
            r += "{:s}: {:.2%}\n".format(str(j), self.freq[j])
        return (self.freq, r)

    def getFreqOf(self, el):
        if el == '*':
            return 1
        f = [self.freq[x] for x in self.freq if el in x]
        return f[0] if f != [] else self.freq[(0)]

class DicePool:
    def __init__(self, s, _raise=False):        
        self.pool = []
        self.modifier = 0
        perr = "Input string must be like 'XdY+Z', got '{:s}' instead."
        s = s.split('+')
        
        for i in s:
            try:
                self.modifier = int(i)
            except ValueError:
                if i[0] == 'd':
                    i = '1'+i
                die = i.split('d')
                self.pool += [Dice(int(die[1])) for x in range(int(die[0]))]
            except:
                raise IOError(perr.format(s,))
                
        
        self.freq = {}
        self.getFreq()
        
        self.values = reduce(lambda a, x: a|x or a,
                             [set(x.vals_n) for x in self.pool],
                             set([]))
        
        self.rise = _raise
    
    def getFreq(self):
        f = self.freq
        if f == {}:
            vals = [x.vals_n for x in self.pool]
            prod = product(*vals)
            
            while True:
                try:
                    el = next(prod)
                    freqs = []
                    
                    for i, e in enumerate(el):
                        freqs.append(self.pool[i].getFreqOf(e))
                        
                    try:
                        f[sum(el)+self.modifier] += reduce(lambda a, x: a*x, freqs)
                    except:
                        f[sum(el)+self.modifier] = reduce(lambda a, x: a*x, freqs)
                except:
                    break
    
        f = {x: f[x] for x in f if f[x] < 1.0}
        r = ''
        for j in sorted(f):
            if f[j] > 1:
                f[j] = 1
            r += "{:s}: {:.2%}\n".format(str(j), f[j])
        return (f, r)

    def getFreqAgainst(self, a, **kwargs):
        a = int(a)
        freqs = self.getFreq()[0]
        suc = reduce( lambda a, x: a+x if a <= 1 else 1,
                     [freqs[x] for x in freqs if x >= a or x == 0],
                      0)
        r = "{:.2%} chance against {:d}".format(suc, a)
        if self.rise:
            r += "\n{:.2%} chance of raise".format(self.getFreqAgainst(a+4)[0])
        return (suc, r)
    

    #pice o' shit!
    def getFreqOfPattern(self, p):
        pass
        # conds = p.split('|')
        # if '{' in p:
        #     wild = DicePool('d6').pool[0]
        # fs = {}
        # for i in conds:
        #     fs[i] = []
        #     elems = i.split('&')
        #     elems = {tuple(eval(x)): 'A' if '[' in x else 'W' for x in elems}
        #     for elem in elems:
        #         fs[i].append(0)
        #         for val in elem:    
        #             if elems[elem] == 'A':
        #                 fs[i][-1] += reduce(lambda a, x: a+x.getFreqOf(val), self.pool, 0)
        #             if elems[elem] == 'W':
        #                 fs[i][-1] += wild.getFreqOf(val)
        #     fs[i] = reduce(lambda a, x: a*x, fs[i])

        # r = 'Chances to get those patterns:\n'
        # for j in sorted(fs):
        #     if fs[j] > 1:
        #         fs[j] = 1
        #     r += "{:s}: {:.2%}\n".format(str(j), fs[j])
        # return (fs, r)

    def challengeInterface(self, s):
        try:
            return self.getFreqAgainst(int(s))
        except ValueError:
            return self.getFreqOfPattern(s) 
        except:
            return "Invalid challenge pattern"

if __name__ == "__main__":
    a = DicePool('2d6')
    print a.challengeInterface(5)
