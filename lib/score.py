# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import db

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

    def set_score(self, musicid, scores, medals):
        self.con.cur.executemany('insert into score values(%s, %s, %s, %s, %s, %s)',
                                 [(self.UID, musicid, dif, self.count, scores[dif], medals[dif]) for dif in range(0, 3)])
                                 
    def update_data(self, username, scoredata):
        self.get_UID(username)
        self.start_updation()
        for music, scores, medals in scoredata:
            self.set_score(music[0], scores, medals)

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
        self.UID = user

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
        self.con.cur.execute('select Date from updation where Count = %s', (self.count,))
        result = self.con.cur.fetchone()
        return result[0]

    def init_musiclist(self):
        self.con.cur.execute('select MusicId, Name from music')
        result = self.con.cur.fetchall()
        self.musiclist = result
    
    def get_score(self, musicid):
        self.con.cur.execute('select Score, Medal from score where UID = %s and MusicId = %s and UpCount = %s order by Difficulty', (self.UID, musicid, self.count))
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
