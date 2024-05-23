import os
import sys
import argparse
import random
from pathlib import Path

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import numbers
from openpyxl.styles import Font
from fnschool.app import *
from fnschool.language import _
from fnschool.fnprint import *
from fnschool.path import *
from fnschool.entry import *
from fnschool.external import *


__version__ = "20240523.80109.809"


# The end.
