import numpy as np
from pcsaft import flashTQ, pcsaft_ares, pcsaft_p

# Toluene
x = np.asarray([1.0])
m = np.asarray([2.8149])
s = np.asarray([3.7169])
e = np.asarray([285.69])
pyargs = {"m": m, "s": s, "e": e}

# Ethane
x = np.asarray([1.0])
m = np.asarray([1.6069])
s = np.asarray([3.5206])
e = np.asarray([191.42])
pyargs = {"m": m, "s": s, "e": e}

t = 300  # K
den = 6.02214076e-4
den = den / (6.02214076e23) * 1e30

ps = flashTQ(t, 0.5, x, pyargs)
print("ps of ethane at {} K : {} Pa".format(t, ps))

ares = pcsaft_ares(t, den, x, pyargs)
print("ares of ethane at {} K {} mol/m3 : {} J/mol".format(t, den, ares))
p = pcsaft_p(t, den, x, pyargs)
print("p of ethane at {} K {} mol/m3 : {} Pa".format(t, den, p))
