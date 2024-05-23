import sys


sys.path.append("../src")
import os
os.environ["PATH"] += os.pathsep +(r"C:\Program Files\Graphviz\bin")
from langtorch import _TextTensor, TextModule
import langtorch
import torch
from langtorch.methods import CoT
# import nnviz


class CustomModule(TextModule):
    def __init__(self):
        super(CustomModule, self).__init__()
        # parent init sets the .content attribute
        self.content2 = TextModule(_TextTensor("2"))
        self.content3 = TextModule(_TextTensor("3"))
        self.content3 = TextModule(_TextTensor("3"))
        self.content4 = CoT
        self.api_call = langtorch.tt.modules.to_tt.activation.OpenAI()

    def forward(self, x):
        return self.content4(self.content3(self.content2(self.content * x)))



torch.Tensor.__torch_function__
x = _TextTensor(torch.randn(1, 3))
batch_size = 2
# device='meta' -> no memory is consumed for visualization


