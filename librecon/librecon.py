#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  librecon.
  Find all vectors
"""
__author__ = 'kall.micke@gmail.com'

from multiprocessing import Process
from librecon.nmap import *
from librecon.dirb import *
from librecon.nikto import *
from librecon.ftp import *
from librecon.sslyze import *
from librecon.quickscan import *
import os

class Librecon:

    def __init__(self):
        pass

    '''
    Initate all recon modules
    '''
    def run(self, ip=''):

        # Starts nmap scan
        np = Nmap(hostname=ip)
        np.scan_stage_1()
        np.scan_stage_2()
        np.scan_stage_3()

        # quick portscan async
        sc = Fullportscan(hostname=ip, silent=True)
        p = Process(target=sc.scan)
        p.start()

        if '21' in np.ports:
            fp = Ftp(hostname=ip)
            fp.run()

        # Port 443 is open spider target.
        if '443' in np.ports:
            nk = Nikto(hostname=ip, ssl_proto=True)
            nk.scan()

            ss = Sslyze(hostname=ip)
            ss.scan()

            db = Dirb(hostname=ip, ssl_proto=True)
            db.robots_scan()
            db.dirb_stage_1()

        # Port 80 is open spider target.
        if '80' in np.ports:
            nk = Nikto(hostname=ip, ssl_proto=False)
            nk.scan()

            db = Dirb(hostname=ip, ssl_proto=False)
            db.robots_scan()
            db.dirb_stage_1()

    '''
    Initate all recon modules
    '''
    def massrecon(self, ip=''):

        print('Not implemented.')
        os._exit(0)

        # Starts nmap scan
        np = Nmap(hostname=ip)
        np.scan_stage_1()
        np.scan_stage_2()
        np.scan_stage_3()

        if '21' in np.ports:
            fp = Ftp(hostname=ip)
            p = Process(target=fp.run)
            p.start()

        # Port 443 is open spider target.
        if '443' in np.ports:
            nk = Nikto(hostname=ip, ssl_proto=True)
            p = Process(target=nk.scan)
            p.start()

            ss = Sslyze(hostname=ip, silent=True)
            p = Process(target=ss.scan)
            p.start()

            p = Process(target=db.robots_scan)
            p.start()

            p = Process(target=db.dirb_stage_1)
            p.start()

        # Port 80 is open spider target.
        if '80' in np.ports:
            nk = Nikto(hostname=ip, ssl_proto=False)
            p = Process(target=nk.scan())
            p.start()

            db = Dirb(hostname=ip, ssl_proto=False, silent=True)

            p = Process(target=db.robots_scan)
            p.start()

            p = Process(target=db.dirb_stage_1)
            p.start()

    '''
    Initiate nmap module only
    '''
    def nmap(self, ip = ''):
        # Starts nmap scan
        np = Nmap(hostname=ip)
        np.scan_stage_1()
        np.scan_stage_2()

    '''
    Initiate Dirb module only
    '''
    def dirb(self, ip = ''):
        # Starts nmap scan
        db = Dirb(hostname=ip, ssl_proto=False)
        db.robots_scan()
        db.dirb_stage_1()

        db = Dirb(hostname=ip, ssl_proto=True)
        db.robots_scan()
        db.dirb_stage_1()
    '''
    Initate Nikto module only
    '''
    def nikto(self, ip=''):

        nk = Nikto(hostname=ip, ssl_proto=False)
        nk.scan()

        nk = Nikto(hostname=ip, ssl_proto=True)
        nk.scan()

    '''
    Initate FTP module only
    '''
    def ftp(self, ip=''):
        fp = Ftp(hostname=ip)
        fp.run()

    '''
    Initate sslyze module only
    '''
    def sslyze(self, ip=''):
        ss = Sslyze(hostname=ip)
        ss.scan()

    '''
    Initate fullportscan module only
    '''
    def quickscan(self, ip=''):
        sc = Quickscan(hostname=ip, silent=True)
        sc.scan()
