import sys

sys.path.append("../src")
from langtorch import _TextTensor, TextModule, Text
from langtorch import Session
import langtorch
import unittest
import numpy as np
import torch

conversation_template = _TextTensor([["{name} says: {greeting}."],
                                     ["{name} replies: {reply}"]])

shared_completion = _TextTensor({"name": "Bob"})
unique_completion = _TextTensor([[{"greeting": "Hello"}],
                                 [{"reply": "Hi there!"}]])

formatted_conversation = conversation_template * shared_completion * unique_completion
print(formatted_conversation)

text = langtorch.Chat(("system", "You are a robot"))
text+= ("user", "I am a human")

print(text)