from tqdm import tqdm
import pickle
import numpy as np
import spistats.desynchronization as dsync

def proba_desync_once(p,m,n):
    packet_count = dsync.NumberOfPacketBeforeDsync(p,m)
    packet_count.eigenvalues()
    return packet_count.cdf(n)

with open("vectors_of_plr.pickle" , 'rb') as f:
    plr = np.array(pickle.load(f))
with open("vectors_of_total.pickle" , 'rb') as f:
    n = np.array(pickle.load(f))

tbl = {}
length = len(n)
for m in [5,10,15,30]:
    P = np.zeros(length).astype(float)
    for i in tqdm(range(length)):
        tmp = proba_desync_once(plr[i],m,n[i])
        if not(np.isnan(tmp)):
            P[i] = tmp
    tbl[m] = np.mean(P)

print(np.sum(np.isnan(P)))
print(tbl)
