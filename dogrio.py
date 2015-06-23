#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2015  Etienne Noreau-Hebert <e@zncb.io>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Willie module that converts doge-speak into dogr.io links
"""

from willie import module
from willie import formatting
import re
import random
from itertools import permutations


dogr_res = ['(very [^.,;:]*)?',
            '(such [^.,;:]*)?',
            '(much [^.,;:]*)?',
            '(so [^.,;:]*)?',
            '(wow)?'];
            
class Dogrio:
    def __init__(self):
        random.seed()
        perms = permutations(dogr_res)
        res = []
        for p in perms:
            np = list(p)
            np[0] = np[0][:-1]
            res.append('[.,;: ]*'.join(np))
        self.regexps = [re.compile(r) for r in res]

    def translate(self,mesg):
        for r in self.regexps:
            m = r.fullmatch(mesg)
            if m:
                break
        #print (m)
        if not m:
            return None
        l = [g for g in list(m.groups()) if g]
        if len(l) < 2:
            return None
        l.append('wow')
        #print(l)
        p = '/'.join([s.translate({ord(' '):None}) for s in l])
        return "http://dogr.io/"+p+".png"

    def colorize(self,mesg):
        cols = [formatting.colors.BLUE,
                formatting.colors.BROWN,
                formatting.colors.CYAN,
                formatting.colors.FUCHSIA,
                formatting.colors.GREEN,
                formatting.colors.GREY,
                formatting.colors.LIGHT_BLUE,
                formatting.colors.LIGHT_CYAN,
                formatting.colors.LIGHT_GREEN,
                formatting.colors.LIGHT_GREY,
                formatting.colors.LIGHT_PURPLE,
                formatting.colors.ORANGE,
                formatting.colors.PURPLE,
                formatting.colors.RED,
                formatting.colors.TEAL,
                formatting.colors.WHITE,
                formatting.colors.YELLOW];
        l = []
        for c in mesg:
            col = random.choice(cols)
            l.append(formatting.color(c,col))
        return ''.join(l)


dogrio_instance = Dogrio()

@module.rule('.*')
def dogrio(bot,trigger):
    mesg = dogrio_instance.translate(trigger.match.group(0));
    if mesg:
        bot.say(dogrio_instance.colorize(mesg))
        
