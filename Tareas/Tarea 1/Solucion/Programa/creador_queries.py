# no correr
exit

import random
phrases = []
with open('medium/database.txt') as oldfile:
    next(oldfile)
    for line in oldfile:
        phrases.append(line)


for i in range(5):
    n =  min(10**(i + 1), len(phrases))
    lines = random.sample(phrases, n)
    with open('medium/querie_' + str(i + 1).zfill(2) + '.txt', 'w') as f:
        f.write(str(n) + "\n")
        for line in lines:
            new_line = line.split(" ", 2)[2][:-1]
            new_line = new_line[:random.randint(0, len(new_line) - 1)]
            f.write(str(len(new_line)) + " " + new_line + "\n")


#tiempos
# 00 0.487
# 01 0.481
# 02 0.483
# 03 0.520
# 04 0.794
# 05 1.917



