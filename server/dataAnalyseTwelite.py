import re

def format_check(s):
    li = s.split(":")
    res = 0

    if( len( li ) == 12 ):
        if( "" == li[0] != li[1] ):
            res = 2
        if( "rc=80000000" != li[2] ):
            res = 3
        if( not re.match("lq=[0-9_]{1,3}",li[3]) ):
            res = 4
        if( not re.match("ct=[A-Z0-9_]{1,4}",li[4]) ):
            res = 5
        if( not re.match("ed=[A-Z0-9_]{8}",li[5]) ):
            res = 6
        if( not re.match("id=[0-9_]{1}",li[6]) ):
            res = 7
        if( not re.match("ba=[0-9_]{4}",li[7]) ):
            res = 8
        if( not re.match("a1=[0-9_]{4}",li[8]) ):
            res = 9
        if( not re.match("a2=[0-9_]{4}",li[9]) ):
            res = 10
        if( not re.match("p0=[0-9_]{1,4}",li[10]) and not re.match("te=[0-9_]{1,4}",li[10]) ):
            res = 11
        if( not re.match("p1=[0-9_]{1,4}",li[11]) and not re.match("hu=[0-9_]{1,5}",li[11]) ):
            res = 12
    else:
        res = 1

    return res
