# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser

class Score(object):
    levellabel = ('Light', 'Medium', 'Beast', 'Nightmare')
    medallabel = ('FAILED', 'CLEAR', 'FC', 'P')
    gradelabel = ('D', 'C', 'B', 'A', 'AA', 'AAA')
    def get_grade(self):
        if   self.score >= 950000: return 5
        elif self.score >= 850000: return 4
        elif self.score >= 700000: return 3
        elif self.score >= 600000: return 2
        elif self.score >= 500000: return 1
        else                     : return 0

    def __init__(self, musicid, title, level, score, medal, ):
        self.musicid = musicid
        self.title = title
        self.level = level
        self.score = score
        self.medal = medal
    def __repr__(self):
        return self.title + "(" + self.levellabel[self.level] + ")" + ": " \
            + str(self.score)  + " " + self.gradelabel[self.get_grade()] \
            + " " + self.medallabel[self.medal]
    def toCSV(self):
        return ",".join([str(self.musicid), self.title, str(self.level), str(self.score), str(self.medal)])

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.nowtag = ''
        self.nowattr = ''
        self.scorelist = []
        self.idflag = False # idを持ってくる時に使うフラグ
        self.musicid = None
        self.title = ''
        self.score = [None] * 4
        self.medal = [None] * 4
        self.inscorearea = False
        self.dif = 0
        HTMLParser.__init__(self)

    def handle_data(self, data):
        if self.nowtag == 'div' or self.nowtag == 'span' or self.nowtag == 'img':
            for name, value in self.nowattr:
                if name == 'class':
                    if value == 'mymusic_tit':
                        self.title += data
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
                    if value == 'nightmare':
                        self.dif = 3

            else:
                for name, value in attr:
                    if name == 'class' and value == 'score_area':
                        self.scorearea_depth = 1
                        self.inscorearea = True
                        self.score = [None] * 4
                        self.medal = [None] * 4
        if tag == 'img':
            self.idflag = False
            for name, value in attr:
                if name == 'class' and value == 'mymusic_jk':
                    self.idflag = True
                    break
            if self.idflag:
                for name, value in attr:
                    if name == 'src':
                        self.musicid = value.split('/')[-1].split('.')[0]

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inscorearea:
                self.scorearea_depth -= 1
                if self.scorearea_depth == 0:
                    for var in range(0, 4):
                        if self.score[var] != None:
                            #             ID  , title     , dif, score          , medal
                            score = Score(self.musicid, self.title, var, self.score[var], self.medal[var])
                            self.scorelist.append(score)
                    self.inscorearea = False
                    self.title = ''
        if tag == self.nowtag:
            self.nowtag = ''
            self.nowattr = ''

    def get_scorelist(self):
        return self.scorelist


# --------- ファイル読み込んでCSVを吐く ---------
def print_csv_from(filename):
    f = open(filename, 'r')
    allLines = f.read()
    f.close()

    parser = MyHTMLParser()
    parser.feed(allLines)
    
    scorelist = parser.get_scorelist()

    print "曲名,難易度,スコア,メダル"
    for score in scorelist:
        # ↓これめっちゃ綺麗でしょ
        # せやなW
        print score.toCSV() 

if __name__ == '__main__' :
    # -------- Light,Medium,Beast -----
    print_csv_from('sample_beast_lmb.html')
    # -------- Nightmare --------------
    print_csv_from('sample_beast_n.html')
