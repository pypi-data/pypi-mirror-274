import sys
import re

sys.path.append("../src")
from langtorch import TextModule, _TextTensor
from langtorch.tt import Activation
from langtorch import Text
from langtorch import Markdown
from langtorch.api.call import chat, auth
import torch
import numpy as np

import logging

Text = Text.from_file("""./assets/paper.md""")
paragraphs = Text.loc["Para"].to_tensor()
paragraphs.embed()

print(paragraphs.embedding)