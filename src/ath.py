#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'qt/utils'))
from utils import text_type

if __name__ == '__main__':
    import lib.Athenum as Athenum
    Athenum.athenumEngineStart()
