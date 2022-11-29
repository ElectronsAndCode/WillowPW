feats = [
        "Talked to Madmartigan in Trap",
        "Learned of Cursed Bridge",
        "Opened Matanda Passage",
        "Met Abang",
        "Dispelled Fin",
        "Nelwyn",
        "Dew",
        "Po's House",
        "Tavern of Traveler",
        "Tir Asleen",
        "Nockmaar Castle",
        "Madmartigan Escaped Trap",
        "Defeated Kael",
        "Defeated Edorsisk",
        "Trap Exit Open",
        "Old Woman on Cliffs",
        "Shipped Sorsha and Madmartigan",
        "Learned of Nail and Wakka",
        "Scared Guard",
        "Bogarda's Cave Guard",
        "Two Towers",
        "Thunder Lady",
        "(Feat 1)",
        "(Feat 2)" ]

shields = [
        "Wooden Shield",
        "Small Shield",
        "Gold Shield",
        "Dragon Shield",
        "Metal Shield",
        "Tail Shield",
        "Battle Shield",
        "Fury Shield" ]

swords = [
        "Long Sword",
        "Battle Sword",
        "Flame Sword",
        "Dragon Sword",
        "Wing Sword",
        "Devileye Sword",
        "Kaiser Sword",
        "Wonder Sword" ]

magics = [
        "Acorn",
        "Bombard",
        "Renew",
        "Thunder",
        "Fireflor",
        "Cane",
        "Terstorm",
        "(Magic 1)",
        "Healmace",
        "Ocarina",
        "Fleet",
        "Specter",
        "Healball",
        "(Magic 2)",
        "(Magic 3)",
        "(Magic 4)" ]

items = [
        "Statue",
        "Ring",
        "Herbs",
        "Scale",
        "Bracelet",
        "Key",
        "Flute",
        "Crystal (Red)",
        "Crystal (Blue)",
        "Crest",
        "Wakka",
        "Nockmaar",
        "Necklace",
        "Powder",
        "Shoes",
        "(Item 1)"
        ]

def endian(val, n):
    r = 0
    for i in range(n):
        r = (r << 8) | (val & 0xff)
        val = val >> 8
    return r

def printbits( val, names, prefix = "" ):
    for x in names:
        if val & 1:
            print prefix + x,
        val = val >> 1
    print

xlat = "ABCDEZabcd0123FGHIJefghi4567KLMNOjkl89!?PQRSTmnopquvwxUVWXYrstyz"

def base64dec(passwd):
    pwd = "".join( [x for x in passwd if not x.isspace()] )
    mx = [ xlat.index(x) for x in pwd]
    return mx

def base64enc(bits):
    p = [ xlat[ x ] for x in bits ]
    s = ""
    while len(p) > 0:
        s += "".join( p[0:3] ) + " "
        p = p[3:]
    s = s[0:11] + "\n" + s[12:]
    return s

key = [5, 25, 50, 33, 5, 25, 50, 33, 5, 25, 50, 33, 5, 25, 50, 33, 5, 25]

def decode_password( c ):
    print c

    c = base64dec( c )

    c[:0] = [0x1f]
    for j in range(len(c)-1,0,-1):
        c[j] = c[j] ^ c[j-1]
    c = c[1:]

    for j in range(len(c)):
        c[j] = (c[j] - key[j]) & 0x3f

    x = sum(c[2:]) & 0x3f
    if x != c[0]:
        print "Sum mismatch",

    x = 0
    for j in range(2,len(c)):
        x = x ^ c[j]
    if x != c[1]:
        print "Xor mismatch",

    c = "".join([ "{:06b}".format(x) for x in c[2:] ])
    print c[0:3], c[3:27], c[27:35], c[35:43], c[43:59], c[59:75], c[75:83], c[83:91], c[91:94], c[94:]

    salt1 = int(c[:3],2)
    c = c[3:]

    ftv = endian( int(c[:24],2), 3 )
    c = c[24:]

    swv = int(c[:8],2)
    c = c[8:]

    shv = int(c[:8],2)
    c = c[8:]

    mgv = endian( int(c[:16],2), 2 )
    c = c[16:]

    itv = endian( int(c[:16],2), 2 )
    c = c[16:]

    v10 = int(c[:8],2)
    c = c[8:]

    lv = int(c[:8],2)
    c = c[8:]

    salt2 = int(c[:3],2)
    c = c[3:]

    empty = c[:2]
    c = c[2:]

    print "First Salt: ", salt1
    print "Feats:      ",
    printbits( ftv, feats, "\n             " )
    print "Swords:     ",
    printbits( swv, swords )
    print "Shields:    ",
    printbits( shv, shields )
    print "Magics:     ",
    printbits( mgv, magics )
    print "Items:      ",
    printbits( itv, items )
    print "V10:        ", v10
    print "Level:      ", lv + 1
    print "Final Salt: ", salt2

    print empty
    print

def create_password( salt1, ftv, swv, shv, mgv, itv, v10, lv, salt2 ):
    """
    Creates a password using the given values

    salt1 - An arbitrary number.  Choose any between 0 and 7
    ftv   - A bitmap of completed feats.  Use the feat array for reference
    swv   - A bitmap of owned swords.  Use the sword array for reference
    shv   - A bitmap of owned shields.  Use the shield array for reference
    mgv   - A bitmap of learned magics.  Use the magic array for reference
    itv   - A bitmap of collected items.  See the item array for reference
    v10   - Possibly unused.  Range 0-255
    lv    - Willow's level.  Range 0-15
    salt2 - A second arbitrary number.  Range 0-7
    """
    bitstream = "{:03b}".format( salt1 )
    bitstream += "{:024b}".format( endian( ftv, 3 ) )
    bitstream += "{:08b}".format( swv )
    bitstream += "{:08b}".format( shv )
    bitstream += "{:016b}".format( endian( mgv, 2 ) )
    bitstream += "{:016b}".format( endian( itv, 2 ) )
    bitstream += "{:08b}".format( v10 )
    bitstream += "{:08b}".format( lv )
    bitstream += "{:03b}".format( salt2 )
    bitstream += "00"

    pw = []
    for x in range(16):
        pw.append( int( bitstream[0:6], 2 ) )
        bitstream = bitstream[6:]

    s = sum( pw ) & 0x3f
    x = 0
    for i in pw:
        x ^= i

    pw[:0] = [ s, x ]

    for i in range(len(pw)):
        pw[i] = (pw[i] + key[i]) & 0x3f

    x = 0x1f
    for i in range(len(pw)):
        pw[i] ^= x
        x = pw[i]

    return base64enc( pw )

#def create_password( salt1, ftv, swv, shv, mgv, itv, v10, lv, salt2 ):
decode_password( create_password( 0, 0b000000000000000000000000,
    0b00000000, 0b00000000, 0b0000000000000000, 0b0000000000000000, 0, 15, 0
    ) )
#decode_password( 
#"""
#0zM yYY iSo
#?3m Qjr 6hD
#""" )

#decode_password( "XDp If3 zyr kHq wmN yrk")
