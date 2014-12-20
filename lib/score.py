# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import db

class ScoreUpdater(object):
    def __init__(self):
        self.con = db.Connection()
        
    def close(self):
        self.con.commit()
        self.con.close()

    def rollback(self):
        self.con.rollback()
        self.con.close()

    def get_UID(self, username):
        self.con.cur.execute('select UID from user where UserName = %s', (username,))
        user = self.con.cur.fetchone()
        self.UID = user['UID']
        
    def start_updation(self):
        self.con.cur.execute('select max(Count) as old_count from updation where UID = %s', (self.UID,))
        result = self.con.cur.fetchone()
        old_count = result['old_count']
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
    def __init__(self):
        self.con = db.Connection()
        self.cur = self.con.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()

    def get_UID(self, username):
        self.cur.execute('select UID from user where UserName = %s', (username,))
        user = self.cur.fetchone()
        self.UID = user

    def get_count(self):
        self.cur.execute('select max(Count) as count from updation where UID = %s', (self.UID,))
        result = self.cur.fetchone()
        self.count = result[0]
        
    def get_musiclist(self):
        self.cur.execute('select MusicId, Name from music')
        result = self.cur.fetchall()
        self.musiclist = result
    
    def get_score(self, musicid):
        self.cur.execute('select Score, Medal from score where UID = %s and MusicId = %s and UpCount = %s order by Difficulty', (self.UID, musicid, self.count))
        result = self.cur.fetchall()
        return result
            
    def get_scoredata(self, username):
        self.get_UID(username)
        self.get_count()
        self.get_musiclist()
        scoredata = []
        for music in self.musiclist:
            musicid = music[0]
            scoredata += [(music, self.get_score(musicid))]
        return scoredata
        
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