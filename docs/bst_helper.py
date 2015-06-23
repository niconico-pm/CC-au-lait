# -*- coding: utf-8 -*-
sl = []

try:
    while True:
        sl += [raw_input()]
except:
    pass

num = 0
txt = list()

for i, s in enumerate(sl):
    line = i % 5
    if line == 0: musicid = s
    if line == 1: title = s
    if line == 2: l = s
    if line == 3: m = s
    if line == 4: 
        b = s
        txt.append(musicid + ',\"' + title + '\"')
        txt.append(musicid + ',0,' + l)
        txt.append(musicid + ',1,' + m)
        txt.append(musicid + ',2,' + b)
        txt.append('insert into music values(' + musicid + ',\"' + title + '\");')
        txt.append('insert into tracks(MusicID, Difficulty, Level) values(' + musicid + ',0,' + l + ');')
        txt.append('insert into tracks(MusicID, Difficulty, Level) values(' + musicid + ',1,' + m + ');')
        txt.append('insert into tracks(MusicID, Difficulty, Level) values(' + musicid + ',2,' + b + ');')
        num = num + 1

print 
for var in range(0, num):
    print txt[var * 8]
print 
for var in range(0, num):
    print txt[var * 8 + 1]
    print txt[var * 8 + 2]
    print txt[var * 8 + 3]
print 
for var in range(0, num):
    print txt[var * 8 + 4]
print 
for var in range(0, num):
    print txt[var * 8 + 5]
    print txt[var * 8 + 6]
    print txt[var * 8 + 7]

#        print "insert into tracks(MusicID, Difficulty, Level) values(%s,%s,%s);" % (musicid, i % 4 - 1, s)
