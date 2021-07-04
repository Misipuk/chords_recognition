"""
Simple chord implementation

Notes
-----
This implementation tries to follow the references and their implementation
(e.g., https://github.com/jayg996/BTC-ISMIR19)
"""
import numpy as np



class Chord:

    def __init__(self, id, start_time, end_time, label):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.label = label

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.start_time, self.end_time, self.label, self.id)