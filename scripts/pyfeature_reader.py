# -*- coding: UTF-8 -*-
"""
translate pyfeature file into feature file
Usage:
    cat <pyfeature_file> | pyfeature_reader.py
"""

import sys
import re

if __name__ == "__main__":
    pattern_feature = re.compile(u'.*with Feature\(u?("|\')(.+)("|\')\)')
    pattern_scenario = re.compile(u'.*with Scenario\(u?("|\')(.+)("|\')\)')
    pattern_step = re.compile(u'.*(given|and_|when|then)\(u?("|\')(.+)("|\').*\)')
    for l in sys.stdin.xreadlines():
        m = pattern_feature.match(l)
        if m:
            print "Feature: " + m.group(2)
        else:
            m = pattern_scenario.match(l)
            if m:
                print " " * 4 + "Scenario: " + m.group(2)
            else:
                m = pattern_step.match(l)
                if m:
                    print " " * 8 + m.group(1).strip("_").capitalize() + " " + m.group(3)


