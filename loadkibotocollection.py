import os
import numpy as np

dirname = r"c:\tf\baduk\aaa"
filenames = os.listdir(dirname)

wnum = 0
bnum = 0

for filename in filenames:
    fullname = os.path.join(dirname, filename)
    ext = os.path.splitext(fullname)[-1]
    if ext == '.kibotfwww':
        wnum += 1

    if ext == '.kibotfbbb':
        bnum += 1
totnum = wnum + bnum

laststate = np.zeros((4 * totnum, 21 * 21 * 3), dtype=np.float32)
komi = np.zeros((4 * totnum, 1), dtype=np.float32)
winner = np.zeros((4 * totnum, 1), dtype=np.float32)

bcount = 0
wcount = 0
totcount = 0
for filename in filenames:
    if totcount % 1000 == 0:
        print('loading rate ', totcount / totnum)
    fullname = os.path.join(dirname, filename)

    f = open(fullname, 'rb')
    ext = os.path.splitext(fullname)[-1]
    komi[4 * totcount + 0, 0] = np.fromstring(f.read(4), dtype='<f4')
    laststate[4 * totcount + 0] = np.fromstring(f.read(), dtype='<f4')

    if ext == '.kibotfwww':
        winner[4 * totcount + 0, 0] = 0.0
        wcount += 1
    if ext == '.kibotfbbb':
        winner[4 * totcount + 0, 0] = 1.0
        bcount += 1

    for x in range(21):
        for y in range(21):
            x1 = 20 - x
            y1 = y
            x2 = x
            y2 = 20 - y
            x3 = 20 - x
            y3 = 20 - y

            laststate[4 * totcount + 1, 21 * 3 * x + 3 * y + 0] = laststate[4 * totcount + 0, 21 * 3 * x1 + 3 * y1 + 0]
            laststate[4 * totcount + 1, 21 * 3 * x + 3 * y + 1] = laststate[4 * totcount + 0, 21 * 3 * x2 + 3 * y2 + 1]
            laststate[4 * totcount + 1, 21 * 3 * x + 3 * y + 2] = laststate[4 * totcount + 0, 21 * 3 * x3 + 3 * y3 + 2]
            laststate[4 * totcount + 2, 21 * 3 * x + 3 * y + 0] = laststate[4 * totcount + 0, 21 * 3 * x1 + 3 * y1 + 0]
            laststate[4 * totcount + 2, 21 * 3 * x + 3 * y + 1] = laststate[4 * totcount + 0, 21 * 3 * x2 + 3 * y2 + 1]
            laststate[4 * totcount + 2, 21 * 3 * x + 3 * y + 2] = laststate[4 * totcount + 0, 21 * 3 * x3 + 3 * y3 + 2]
            laststate[4 * totcount + 3, 21 * 3 * x + 3 * y + 0] = laststate[4 * totcount + 0, 21 * 3 * x1 + 3 * y1 + 0]
            laststate[4 * totcount + 3, 21 * 3 * x + 3 * y + 1] = laststate[4 * totcount + 0, 21 * 3 * x2 + 3 * y2 + 1]
            laststate[4 * totcount + 3, 21 * 3 * x + 3 * y + 2] = laststate[4 * totcount + 0, 21 * 3 * x3 + 3 * y3 + 2]

    komi[4 * totcount + 1, 0] = komi[4 * totcount + 0, 0]
    komi[4 * totcount + 2, 0] = komi[4 * totcount + 0, 0]
    komi[4 * totcount + 3, 0] = komi[4 * totcount + 0, 0]
    winner[4 * totcount + 1, 0] = winner[4 * totcount + 0, 0]
    winner[4 * totcount + 2, 0] = winner[4 * totcount + 0, 0]
    winner[4 * totcount + 3, 0] = winner[4 * totcount + 0, 0]

    totcount = totcount + 1
    f.close()

laststate_collectionname = r"c:\tf\baduk\laststate_kibotfcollection.npy"
komi_collectionname = r"c:\tf\baduk\komi_kibotfcollection.npy"
winner_collectionname = r"c:\tf\baduk\winner_kibotfcollection.npy"

np.save(laststate_collectionname, laststate.T)
np.save(komi_collectionname, komi.T)
np.save(winner_collectionname, winner.T)

