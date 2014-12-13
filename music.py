# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib2

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.nowtag = ''
        self.nowattr = ''
        self.scorelist = []
        self.music = [None, '']
        self.score = [None] * 3
        self.medal = [None] * 3
        self.inscorearea = False
        self.dif = 0
        HTMLParser.__init__(self)

    def handle_data(self, data):
        if self.nowtag == 'div' or self.nowtag == 'span' or self.nowtag == 'img':
            for name, value in self.nowattr:
                if name == 'class':
                    if value == 'mymusic_tit':
                        self.music[1] += data
                    else:
                        if value == 'score_num':
                            self.score[self.dif] = data
                        if value == 'perfect':
                            self.medal[self.dif] = 3
                        if value == 'fullcombo':
                            self.medal[self.dif] = 2
                        if value == 'clear':
                            self.medal[self.dif] = 1
                        if value == 'failed':
                            self.medal[self.dif] = 0
    
    def handle_starttag(self, tag, attr):
        self.nowtag = tag
        self.nowattr = attr
        if tag == 'div':
            if self.inscorearea:
                self.scorearea_depth += 1
                for name, value in attr:
                    if value == 'light':
                        self.dif = 0
                    if value == 'medium':
                        self.dif = 1
                    if value == 'beast':
                        self.dif = 2
            else:
                for name, value in attr:
                    if name == 'class' and value == 'score_area':
                        self.scorearea_depth = 1
                        self.inscorearea = True
                        self.score = [None] * 3
                        self.medal = [None] * 3
        if tag == 'img':
            flag = False
            for name, value in attr:
                if name == 'class' and value == 'mymusic_jk':
                    flag = True
                    break
            if flag:
                for name, value in attr:
                    if name == 'src':
                        self.music[0] = value.split('/')[-1].split('.')[0]
                        print self.music

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inscorearea:
                self.scorearea_depth -= 1
                if self.scorearea_depth == 0:
                    self.scorelist.append((tuple(self.music),tuple(self.score),tuple(self.medal)))
                    self.inscorearea = False
                    self.music[0] = None
                    self.music[1] = ''
        if tag == self.nowtag:
            self.nowtag = ''
            self.nowattr = ''

    def get_scorelist(self):
        return self.scorelist

f = open('sample_beast.html', 'r')
allLines = f.read()
f.close()
f = open('music_data.csv', 'w')


parser = MyHTMLParser()
parser.feed(allLines)

scorelist = parser.get_scorelist()
#print scorelist
song_num = 0
l_num = 0
m_num = 0
b_num = 0
l_total = 0
m_total = 0
b_total = 0
lp = 0
lf = 0
lc = 0
lb = 0
mp = 0
mf = 0
mc = 0
mb = 0
bp = 0
bf = 0
bc = 0
bb = 0
ln = 0
mn = 0
bn = 0
for score in scorelist:
    f.write(str(score[0][0]) + "," + score[0][1] + "\n")
    print "曲名   :", score[0][0], score[0][1]
    print "Light  :", score[1][0], score[2][0]
    print "Medium :", score[1][1], score[2][1]
    print "Beast  :", score[1][2], score[2][2]
    if score[1][0] != None:
        l_total += int(score[1][0])
        l_num += 1
    if score[1][1] != None:
        m_total += int(score[1][1])
        m_num += 1
    if score[1][2] != None:
        b_total += int(score[1][2])
        b_num += 1
    if score[2][0] != None:
        if score[2][0] == 3:
            lp += 1
        if score[2][0] == 2:
            lf += 1
        if score[2][0] == 1:
            lc += 1
        if score[2][0] == 0:
            lb += 1
    else:
        ln += 1
    if score[2][1] != None:
        if score[2][1] == 3:
            mp += 1
        if score[2][1] == 2:
            mf += 1
        if score[2][1] == 1:
            mc += 1
        if score[2][1] == 0:
            mb += 1
    else:
        mn += 1
    if score[2][2] != None:
        if score[2][2] == 3:
            bp += 1
        if score[2][2] == 2:
            bf += 1
        if score[2][2] == 1:
            bc += 1
        if score[2][2] == 0:
            bb += 1
    else:
        bn += 1
    song_num += 1
print "Total Score"
print "Light  :", l_total
print "Medium :", m_total
print "Beast  :", b_total
print "Total  :", l_total + m_total + b_total
print "Average Score"
print "Light  :", l_total / song_num
print "Medium :", m_total / song_num
print "Beast  :", b_total / song_num
print "Average Score(プレイ済み)"
print "Light  :", l_total / l_num
print "Medium :", m_total / m_num
print "Beast  :", b_total / b_num
print "Clear Medal"
print "Medal     : Light, Medium, Beast"
print "Perfect   :", lp, ",", mp, ",", bp
print "FullCombo :", lf, ",", mf, ",", bf
print "Clear     :", lc, ",", mc, ",", bc
print "Failed    :", lb, ",", mb, ",", bb
print "NoPlay    :", ln, ",", mn, ",", bn
f.close()
