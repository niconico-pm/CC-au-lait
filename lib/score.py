# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import db

class Score(object):
    diflabels = ('Light', 'Medium', 'Beast', 'Nightmare')
    medallabels = ('FAILED', 'CLEAR', 'FC', 'P')
    gradelabels = ('D', 'C', 'B', 'A', 'AA', 'AAA')
    def __init__(self, musicid, title, dif, score, medal, level):
        self.musicid = (musicid if isinstance(musicid, long) else long(musicid))
        self.title = (title if isinstance(title, str) else title.encode('utf-8'))
        self.dif = dif
        self.score = score
        self.medal = medal
        self.level = level
    def get_grade(self):
        if   self.score >= 950000: return 5
        elif self.score >= 850000: return 4
        elif self.score >= 700000: return 3
        elif self.score >= 600000: return 2
        elif self.score >= 500000: return 1
        else                     : return 0
    def get_diflabel(self):
        return self.diflabels[self.dif]
    def get_gradelabel(self):
        return self.gradelabels[self.get_grade()]
    def get_medallabel(self):
        return self.medallabels[self.medal]
    def __repr__(self):
        return "%d %s(%s): %d %s %s %s" % \
            (self.musicid, self.title, self.get_diflabel(), self.score, self.get_gradelabel(), self.get_medallabel(), self.level)
    def __str__(self):
        return "%d %s %s %s" % (self.score, self.get_gradelabel(), self.get_medallabel(), self.level)
    def toCSV(self):
        return ",".join([str(self.musicid), self.title, str(self.level), str(self.score), str(self.medal)])

class ScoreTable(object):
    # tableにmusicidをkeyとする[l, m, b, n]のScoreのListを格納
    # titlesにmusicidをkeyとして一番最初に来たtitleを格納
    def __init__(self):
        self.table = dict()
        self.titles = dict()
    def add(self, score):
        if not self.table.has_key(score.musicid):
            self.table[score.musicid] = [None] * 4
            self.titles[score.musicid] = score.title
        self.table[score.musicid][score.dif] = score
    def add_list(self, scorelist):
        for score in scorelist:
            self.add(score)
    def add_from_getterdata(self, scoredata):
        for music, tupled_scores in scoredata:
            musicid, title = music
            for dif, tupled_score in enumerate(tupled_scores):
                if not tupled_score[0] is None:
                    score = Score(musicid, title, dif, *tupled_score)
                    self.add(score)
    def __repr__(self):
        s = ""
        for musicid, l in self.table.iteritems():
            title = self.titles[musicid]
            s += "%s(%s): " % (title[:15].ljust(10), musicid)
            for score in l:
                s += (str(score).rjust(20)+"\t") if not score is None else (" ".rjust(20) + "\t")
            s += "\n"
        return s

class ScoreUpdater(object):
    def __init__(self):
        self.con = db.SimpleConnection()
        
    def close(self):
        self.con.commit()
        self.con.close()

    def rollback(self):
        self.con.rollback()
        self.con.close()

    def get_UID(self, username):
        self.con.cur.execute('select UID from user where UserName = %s', (username,))
        user = self.con.cur.fetchone()
        self.UID, = user       # unpack tuple
        
    def start_updation(self):
        self.con.cur.execute('select max(Count) from updation where UID = %s', (self.UID,))
        result = self.con.cur.fetchone()
        old_count, = result
        if old_count == None:
            count = 0
        else:
            count = old_count + 1
        self.con.cur.execute('insert into updation(Count, UID) values(%s, %s)', (count, self.UID))
        self.count = count

    def set_scores(self, musicid, scores):
        self.con.cur.executemany('insert into score values(%s, %s, %s, %s, %s, %s)',
                                [(self.UID, musicid, dif, self.count, score.score if not score is None else None, score.medal if not score is None else None) for dif, score in enumerate(scores)])
        # !!!!!!!!!for debug!!!!!!!!!!!!!
        # print [(self.UID, musicid, dif, self.count, score.score if not score is None else None, score.medal if not score is None else None) for dif, score in enumerate(scores)]
    
    def update_data(self, username, scoretable):
        self.get_UID(username)
        self.start_updation()
        for musicid, scores in scoretable.table.iteritems():
            self.set_scores(musicid, scores)

class ScoreGetter(object):
    def __init__(self, username):
        self.con = db.SimpleConnection()
        self.init_UID(username)
        self.count = self.get_maxcount()

    def close(self):
        self.con.close()

    def init_UID(self, username):
        self.con.cur.execute('select UID from user where UserName = %s', (username,))
        user = self.con.cur.fetchone()
        self.UID, = user

    def get_maxcount(self):
        self.con.cur.execute('select max(Count) from updation where UID = %s', (self.UID,))
        result = self.con.cur.fetchone()
        self.maxcount,  = result
        return self.maxcount

    def set_count(self, count):
        if self.maxcount == None: return False
        if count < 0:
            count += self.maxcount + 1

        if count < 0 or count > self.maxcount:
            return False
        else:
            self.count = count
            return True

    def get_date(self):
        self.con.cur.execute('select Date from updation where UID = %s and Count = %s', (self.UID, self.count))
        result = self.con.cur.fetchone()
        return result[0]

    def init_musiclist(self):
        self.con.cur.execute('select MusicId, Name from music')
        result = self.con.cur.fetchall()
        self.musiclist = result
    
    def get_score(self, musicid):
        self.con.cur.execute('select s.Score, s.Medal, t.Level from (select * from tracks where MusicID = %s) as t left outer join (select * from score where UID = %s and MusicID = %s and UpCount = %s) as s on t.Difficulty = s.Difficulty order by s.Difficulty', (musicid, self.UID, musicid, self.count))
        result = self.con.cur.fetchall()
        return result

    def get_scoredata(self):
        self.init_musiclist()
        return [(music, self.get_score(music[0])) for music in self.musiclist]

class ScoreParser(HTMLParser):
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
                            self.score[self.dif] = int(data)
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
                    for dif in range(0, 4):
                        if self.score[dif] != None:
                            #             ID          , title     , dif, score          , medal          , level
                            score = Score(self.musicid, self.title, dif, self.score[dif], self.medal[dif], None)
                            self.scorelist.append(score)
                    self.inscorearea = False
                    self.title = ''
        if tag == self.nowtag:
            self.nowtag = ''
            self.nowattr = ''

    def get_scorelist(self):
        return self.scorelist
