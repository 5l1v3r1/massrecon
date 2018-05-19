#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Dirb
   Module for spidering target
"""
__author__ = 'kall.micke@gmail.com'

import subprocess
import time
import os
import re
import signal
import sys

from librecon.configuration import *
from librecon.cherrytree import *
from librecon.utils import *
from halo import Halo
from librecon.colors import *

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print("\nYou pressed Ctrl+C!")
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


class Dirb:

    def __init__(self, hostname='', ssl=False):

        self.hostname = hostname
        self.module_disable = False
        self.directory_log = False
        self.ssl = ssl

        self.chr = CherryTree(address=hostname)

        # Load configuration
        self.cfg = Configuration()

        self.config_dir = self.cfg.config_dir

        if os.path.isfile('/usr/bin/dirb') is False:
            utils.puts('info', 'Dirb is not installed')
            self.module_disable = True
            return

        if self.cfg.config.get('massrecon', 'directory_log') == 'True':
            self.directory_log = True

        if self.cfg.config.get('massrecon', 'cherrytree_log') == 'True':
            self.cherrytree_log = True

        if len(self.hostname) == 0:
            utils.puts('warning', 'No host to spider')
            return

        self.scanfolder = '%s/results/dirb/%s' % (self.config_dir, self.hostname)

        if self.directory_log is True:
            self.dirb_dir = '%s/results/%s/dirb' % (self.config_dir, self.hostname)
            if os.path.isdir(self.dirb_dir) is False:
                os.makedirs(self.dirb_dir, exist_ok=True)

        self.wordlist = self.cfg.config.get('massrecon', 'dirb_wordlist')


    def dirb_stage_1(self):

        color = Colors()
        output = ''

        if self.module_disable is True:
            return

        # Nmap stage1
        with Halo(text='%sDIRB STAGE%s' % (color.blue, color.reset), spinner='dots'):

            if self.ssl is True:
                proto = 'https'
            else:
                proto = 'http'

            try:
                if self.directory_log is True:
                    output = subprocess.getoutput("dirb %s://%s %s -w -X .php,.txt,.sh -o %s/dirb_stage1" % (proto, self.hostname, self.wordlist, self.dirb_dir))
                else:
                    output = subprocess.getoutput("dirb %s://%s %s -w -X .php,.txt,.sh" % (proto, self.hostname, self.wordlist))
            except:
                pass

        if len(output) > 2:
            print("\n")
            print("%s=%s" % (color.red, color.reset) * 90)
            print("%s DIRB_STAGE_1: %s %s" % (color.yellow, self.hostname, color.reset))
            print("%s=%s" % (color.red, color.reset) * 90)
            print('%s%s%s' % (color.green, output, color.reset))
            print("%s-%s" % (color.red, color.reset) * 90)
            print("\n")

        if self.cherrytree_log is True and len(output) > 2:

            _leaf_name = 'dirb_stage_%s' % time.strftime("%Y%m%d_%H:%M:%S")

            self.chr.insert(name='machines', leaf=self.hostname)
            self.chr.insert(name=self.hostname, leaf=_leaf_name, txt=output)
