#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  CherryTree class
"""
__author__ = 'kall.micke@gmail.com'

import sqlite3
import time
import os

from configuration import *
from utils import *


class CherryTree:

    def __init__(self):

        self.LEVEL = {'root': 0, 'host': 1, 'recon': 2, 'nmap': 3}

        # Load configuration
        cfg = Configuration()

        if cfg.config.get('massrecon', 'cherrytree_log') != 'True':
            utils.puts('info', 'CherryTree module is disabled')
            return

        db_file = '%s/massrecon.ctb' % cfg.config_dir

        if os.path.exists(db_file) is False:
            utils.puts('info', 'CherryTree database not found. Created it.')
            self.conn = sqlite3.connect(db_file)
            self.setup_database()
        else:
            self.conn = sqlite3.connect(db_file)

    def setup_database(self):

        self.conn.execute('CREATE TABLE IF NOT EXISTS bookmark (node_id INTEGER, sequence INTEGER)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS children (node_id INTEGER, father_id INTEGER, sequence INTEGER)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS codebox (node_id INTEGER, offset INTEGER, justification TEXT, txt TEXT, syntax TEXT, width INTEGER, height INTEGER, is_width_pix INTEGER, do_highl_bra INTEGER, do_show_linenum INTEGER)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS grid (node_id INTEGER, offset INTEGER, justification TEXT, txt TEXT, col_min INTEGER, col_max INTEGER)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS image (node_id INTEGER, offset INTEGER, justification TEXT, anchor TEXT, png BLOB, filename TEXT, link TEXT, time INTEGER)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS node (node_id INTEGER, name TEXT, txt TEXT, syntax TEXT, tags TEXT, is_ro INTEGER, is_richtxt INTEGER, has_codebox INTEGER, has_table INTEGER, has_image INTEGER, level INTEGER, ts_creation INTEGER, ts_lastsave INTEGER)')

        self.insert('root', 'machines')

    def insert(self, on_level='', data=''):

        if len(data) == 0:
            return

        # Avoid duplicates
        if on_level == 'host':
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT name FROM node WHERE name='%s'" % data)
                tb_name = str(cur.fetchone()[0])
                if tb_name == data:
                    cur.close()
                    return
                cur.close()
            except:
                pass

        if on_level not in self.LEVEL.keys():
            utils.puts('info', 'The input level do not match the levels configured')
            return False

        try:
            cur = self.conn.cursor()
            cur.execute('SELECT max(node_id) FROM node')
            node_id = int(cur.fetchone()[0]) + 1
            cur.close()
        except:
            node_id = 1

        # Configures default values
        epoch = time.mktime(time.localtime())

        name = data
        txt = '<?xml version="1.0"?><node><rich_text></rich_text></node> '
        syntax = 'customer-colors'
        tags = 0
        is_ro = 0
        is_rightxt = 0
        has_codebox = 0
        has_table = 0
        has_image = 0
        level = 0
        ts_creation = epoch
        ts_lastsave = epoch

        _sql = "INSERT INTO node VALUES (%s, '%s','%s', '%s', %s, %s, %s, %s, %s, %s, %s, '%s', '%s')" % (node_id,
                                                                                                          name,
                                                                                                          txt,
                                                                                                          syntax,
                                                                                                          tags,
                                                                                                          is_ro,
                                                                                                          is_rightxt,
                                                                                                          has_codebox,
                                                                                                          has_table,
                                                                                                          has_image,
                                                                                                          level,
                                                                                                          ts_creation,
                                                                                                          ts_lastsave)
        # Add node
        cur = self.conn.cursor()
        cur.execute(_sql)
        self.conn.commit()

        # Add children
        _sql = "INSERT INTO children VALUES (%s,%s,%s)" % (node_id, self.LEVEL[on_level], 1)
        cur.execute(_sql)
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == '__main__':


    stage_1 = """✔ 631/tcp open
✔ 7000/tcp open
    """
    #print(stage_1)

    stage_2 = """
Starting Nmap 7.70 ( https://nmap.org ) at 2018-05-02 15:34 CEST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000069s latency).

PORT     STATE SERVICE VERSION
631/tcp  open  ipp     CUPS 2.2
| http-methods: 
|_  Potentially risky methods: PUT
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: CUPS/2.2 IPP/2.1
|_http-title: Home - CUPS 2.2.7
7000/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.42 seconds
"""

    #print(stage_2)

    chr = CherryTree()
    chr.insert('host', '127.0.0.1')
    chr.insert('nmap', stage_2)
    chr.close()
