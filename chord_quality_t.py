from enum import Enum

class ChordQuality(Enum):
    cq_unknown = 0
    cq_major = 0
    cq_minor = 1
    cq_5 = 2
    cq_7th = 3
    cq_major_7th = 4
    cq_minor_7th = 5
    cq_sus2 = 6
    cq_sus4 = 7
    cq_hdim7 = 8
    cq_aug = 9
    cq_dim = 10
    cq_dim7 = 11
    #end of min supported set
    cq_maj_add9 = 12
    cq_min_add9 = 13
    cq_maj6 = 14
    cq_min6 = 15
    cq_maj9 = 16
    cq_min9 = 17
    cq_maj_add11 = 18
    cq_7_add9sharp = 19
    cq_9 = 20
    cq_aug7 = 21
    cq_maj11 = 22
    cq_min11 = 23
    cq_maj13 = 24
    cq_min13 = 25
    cq_Min = cq_dim7
    cq_Max = cq_min13