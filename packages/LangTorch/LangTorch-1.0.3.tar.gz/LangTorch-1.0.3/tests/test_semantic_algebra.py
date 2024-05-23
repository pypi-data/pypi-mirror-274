import sys
import re

sys.path.append("../src")
from langtorch import Text
from langtorch import _TextTensor, OpenAI
import langtorch
import torch
import numpy as np


paper = Text.from_file("""./assets/paper.md""").loc["Para"].to_tensor()

for p in paper.content:
    print(str(p)[:46] + "...")

from langtorch.tt import Activation, TextModule

input_emails = _TextTensor(["""Hello,
I have discovered a major security vulnerability in your system. Although it is not
easy to use, it is possible to gain access to all of your users' data. I have attached
a proof of concept. Please fix this issue as soon as possible.
Cheers, Donny"""]) # and so on and so on
task = TextModule("{*}\n\nClassify the above email as IMPORTANT or NOT IMPORTANT as it relates to a software company. Don't answer right away. First, provide your reasoning step by step.",
                  OpenAI("gpt-3.5-turbo", T=1.1, n = 9, max_tokens = 300))
ensample_answers = task(input_emails)
print(ensample_answers.shape)
answer= langtorch.mean(ensample_answers, dim=-1)
print(ensample_answers, answer)


task = TextModule("Rewrite this paragraph of a paper to sound like the pizzeria mamma mia ramblings of a funny italian man:\n", Activation())

mean_paragraph = langtorch.max(paper, dim=0)

# Output:
# Our analysis delves into the capabilities and limitations of AI language models like GPT-3,emphasizing
# the importance of understanding their statistical foundations and the implications of their output.
# These models, while powerful in their ability to generate text, operate within a framework of modal truth
# rather than absolute reality. This distinction raises concerns about the societal impact of widespread adoption,
# particularly in fields such as journalism and translation. The potential dangers highlighted in our discussion underscore
# the need for a nuanced approach to the use of AI-generated content to maintain the integrity of our informational landscape.