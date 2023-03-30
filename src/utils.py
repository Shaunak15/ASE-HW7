import math
import random
from num import Num
import sys
import re
import inputs

def cli(options):
    for k, v in options.items():
        v = str(v)
        for n, x in enumerate(sys.argv):
            if x== "-" + k[0] or x == "--" + k:
                v = (sys.argv[n + 1] if n + 1 < len(
                    sys.argv) else False) or v == "False" and "true" or v == "True" and "false"
            options[k] = coerce(v)
    return options

def coerce(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            pass

    if s == "true" or s == "True":
        return True
    elif s == "false" or s == "False":
        return False
    else:
        return s

def settings(s):
    t={}
    res = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
    for k,v in res:
            t[k] = coerce(v)
    return t


def erf(x):
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)
    t = 1 / (1 + (p * x))
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y

def gaussian(mu = 0, sd = 1):
    sq = math.sqrt
    pi = math.pi
    log = math.log
    cos = math.cos
    r = random.random
    return mu + sd * sq(-2 * log(r())) * cos(2 * pi * r())

def samples(t, n = None):
    u = []
    for i in range(n or len(t)):
        u.append(random.choice(t))
    return u

def cliffsDelta(ns1, ns2):
    n, gt, lt = 0, 0, 0
    if len(ns1) > 128: ns1 = samples(ns1, 128)
    if len(ns2) > 128: ns2 = samples(ns2, 128)
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y: gt += 1
            if x < y: lt += 1
    return abs(lt - gt) / n <= inputs.the['cliff']

def delta(i, other):
    e, y, z = 1E-32, i, other
    return abs(y.mu - z.mu) / (math.sqrt(e + y.sd ** 2 / y.n + z.sd ** 2 / z.n))

def bootstrap(y0, z0):
    x, y, z, yhat, zhat = Num(), Num(), Num(), [], []
    for y1 in y0:
        Num.add(x, y1)
        Num.add(y, y1)
    for z1 in z0:
        Num.add(x, z1)
        Num.add(z, z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    for y1 in y0: yhat.append(y1 - ymu + xmu)
    for z1 in z0: zhat.append(z1 - zmu + xmu)
    tobs = delta(y, z)
    n = 0
    for i in range(inputs.the['bootstrap']):
        if (delta(Num(samples(yhat)), Num(samples(zhat))) > tobs):
            n += 1
    return n / inputs.the['bootstrap'] >= inputs.the['conf']

def RX(t, s = None):
    t.sort()
    return {"name": s or "", "rank": 0, "n": len(t), "show": "", "has": t}

def mid(t):
    t = t["has"] if "has" in t else t
    n = len(t) // 2
    return len(t) % 2 == 0 and (t[n] + t[n + 1]) / 2 or t[n + 1]

def div(t):
    t = t["has"] if "has" in t else t
    return (t[len(t) * 9 // 10] - t[len(t) * 1 // 10]) / 2.56

def merge(rx1, rx2):
    rx3 = RX([], rx1["name"])
    for t in (rx1["has"], rx2["has"]):
        for x in t:
            rx3["has"].append(x)
    rx3["has"].sort()
    rx3["n"] = len(rx3["has"])
    return rx3

def scottKnot(rxs):
    def merges(i, j):
        out = RX([], rxs[i]["name"])
        for _ in range(i, j+1):
            out = merge(out, rxs[j])
        return out
    
    def same(lo, cut, hi):
        l, r = merges(lo, cut), merges(cut+1, hi)
        return cliffsDelta(l['has'], r['has']) and bootstrap(l['has'], r['has'])
    
    def recurse(lo, hi, rank):
        cut, b4, best = None, merges(lo, hi), 0
        for j in range(lo, hi+1):
            if j < hi:
                l, r = merges(lo, j), merges(j+1, hi)
                now = (l["n"] * (mid(l) - mid(b4)) ** 2 + r["n"] * (mid(r) - mid(b4)) ** 2) / (l["n"] + r["n"])
                if now > best:
                    if abs(mid(l) - mid(r)) >= cohen:
                        cut, best = j, now
        if cut and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank  = recurse(cut + 1, hi, rank)
        else:
            for i in range(lo, hi + 1):
                rxs[i]["rank"] = rank
        return rank
    rxs.sort(key=lambda x: mid(x))
    cohen = div(merges(0, len(rxs) - 1)) * inputs.the['cohen']
    recurse(0, len(rxs) - 1, 1)
    return rxs

def tiles(rxs):
    huge, min_f, max_f, floor = float("inf"), min, max, math.floor
    lo, hi = huge, -huge
    for rx in rxs:
        lo = min_f(lo, rx["has"][0])
        hi = max_f(hi, rx["has"][-1])
    for rx in rxs:
        t, u = rx["has"], []
        def of(x, most): 
            return max(1, min_f(most, x))
        def at(x): 
            return t[of(int(len(t) * x), len(t) - 1)]
        def pos(x): 
            return floor(of(inputs.the['width'] * (x - lo) / (hi - lo + 1E-32) // 1,inputs.the['width']))
        
        for _ in range(inputs.the['width']): 
            u.append(" ")
        a, b, c, d, e= at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E= pos(a), pos(b), pos(c), pos(d), pos(e)
        for i in range(A, B):
            u[i] = "-"
        for i in range(D, E):
            u[i] = "-"
            
        u[inputs.the['width'] // 2] = "|"
        u[C] = "*"
        rx["show"] = "".join(u) + " { %6.2f" % a  + "}"
        for x in (b, c, d, e):
            rx["show"] += ", %6.2f" % a
        rx["show"] += " }"
    return rxs