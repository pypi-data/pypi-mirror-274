import sys

sys.path.append("../src")
from langtorch import _TextTensor, TextModule
from langtorch import Session
from langtorch import Markdown
import langtorch
import langtorch.tt as tt
import unittest
import numpy as np
import torch

print(*map(lambda x: x+1, torch.ones(5,5)))