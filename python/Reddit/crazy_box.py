
from itertools import permutations
from copy import deepcopy
from random import shuffle

boxCeption = False  # Boooooo!!!

boxes = []
stacked = []
filled = []


def boxify(s):  # Take a 3-dimensional scratchpad and revert to box
    return (len(s), len(s[0]), len(s[0][0]))


def stackify(b):  # take box and create scratchpad
    return[[[True for _ in range(b[2])] for _ in range(b[1])] for _ in range(b[0])]


def fits(b, s):  # Determine if a given box fits inside a scratchpad
    bx, by, bz = b
    sx, sy, sz = boxify(s)
    if b == boxify(s):  # Disallow exact matches
        return False
    for x in range(sx - bx + 1):  # Simple scratchpad matching
        for y in range(sy - by + 1):
            for z in range(sz - bz + 1):
                good = True
                for i in range(x, x + bx):
                    for j in range(y, y + by):
                        for k in range(z, z + bz):
                            if not s[i][j][k]:
                                good = False
                if good:
                    return(x, y, z)  # \o/ it fits
    if b == (1, 1, 1):
        print(b, s)
    return False


def put(b, rot, s, pos):  # Take a rotated box fit, and update our state
    px, py, pz = pos
    bx, by, bz = rot
    for x in range(px, px + bx):
        for y in range(py, py + by):
            for z in range(pz, pz + bz):
                s[x][y][z] = False


# Input reading happens here
stacked.append(stackify(tuple(map(int, input().split()))))

input()

while True:
    try:
        boxes.append(tuple(map(int, input().split())))
    except:
        break

done, lmax, best, reps, old = False, -1, None, 10, (stacked, boxes)

for _ in range(reps):
    stacked, boxes = deepcopy(old)
    filled = []
    desc = []
    shuffle(boxes)
    while True:  # Keep trying to fit more boxs
        updates = []
        for stack in stacked:
            for box in boxes:
                fs = [(p, fits(p, stack))
                      for p in permutations(box) if fits(p, stack)]  # Rotations!
                if len(fs) > 0:
                    rot, fit = fs[0]
                    put(box, rot, stack, fit)
                    desc.append("Insert box {} into {} at {} rotated to {}".format(
                        box, boxify(stack), fit, rot))  # Sanity
                    updates.append(box)
        if len(updates) == 0:
            break
        for b in updates:  # Put box in the stackable pile
            boxes.remove(b)
            filled.append(b)
            if boxCeption:
                stacked.append(stackify(b))
    if len(filled) > lmax:
        lmax, best = len(filled), (filled, desc)

filled, desc = best

print("\n".join(desc))

print(
    "===========================================================================")
print("Filled {} boxes into the {} {} {}:".format(
    len(filled), *boxify(stacked[0])))  # Output wooo
for b in filled:
    print(b)
