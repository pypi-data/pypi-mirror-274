import os
import sys


class Currency:
    def __init__(self, name=None, unit=None, mark=None):
        self.name = name
        self.unit = unit
        self.mark = mark

    @property
    def CNY(self):
        CNY = Currency("CNY", "CNY", "¥")

        return CNY
