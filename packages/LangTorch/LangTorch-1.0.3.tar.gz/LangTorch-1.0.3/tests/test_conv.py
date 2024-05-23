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

#
# class TestMul(unittest.TestCase):
#     def test_mul1(self):
#         tensor1 = TextTensor("1")
#         tensor1.requires_grad = True
#         tensor2 = TextTensor("2")
#         tensor2.requires_grad = True
#         tensor3 = tensor2*tensor1
#         tensor3.backward()
#         self.assertTrue((tensor2.grad == tensor1) and (tensor1.grad == tensor2))
#
#
# if __name__ == "__main__":
#     unittest.main()


import torch
import torch.nn as nn
import numpy as np
from typing import Tuple


def unfold(array, dimension, size, step):
    # This function will unfold along a specified dimension with a given size and step (stride)

    # Compute the shape of the resulting "unfolded" array
    new_shape = list(array.shape)
    num_blocks = (new_shape[dimension] - size) // step + 1
    new_shape[dimension] = num_blocks
    new_shape.insert(dimension + 1, size)
    unfolded_array = np.full(new_shape, None, dtype=object)

    # Fill the unfolded array with windows of the original array
    for i in range(num_blocks):
        start_idx = i * step
        end_idx = start_idx + size
        unfolded_array[..., i, :] = array.take(indices=range(start_idx, end_idx), axis=dimension)

    return unfolded_array

def unfold(array, dimension, size, step):
    new_shape = list(array.shape)
    num_blocks = (new_shape[dimension] - size) // step + 1
    new_shape[dimension] = num_blocks
    new_shape.insert(dimension + 1, size)
    unfolded_array = np.full(new_shape, None, dtype=object)
    for i in range(num_blocks):
        start_idx = i * step
        end_idx = start_idx + size
        unfolded_array[..., i, :] = array.take(indices=range(start_idx, end_idx), axis=dimension)
    return unfolded_array

class ManualConvolution(nn.Module):
    def __init__(self,
                 content: _TextTensor,
                 in_channels: int,
                 out_channels: int,
                 kernel_size: Tuple[int, ...],
                 stride: Tuple[int, ...],
                 padding: Tuple[int, ...],
                 dilation: Tuple[int, ...],
                 transposed: bool,
                 output_padding: Tuple[int, ...],
                 groups: int,
                 bias: bool,
                 padding_mode: str):
        super(ManualConvolution, self).__init__()
        # Store all parameters, even though not all are used
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.transposed = transposed
        self.output_padding = output_padding
        self.groups = groups
        self.bias = bias
        self.padding_mode = padding_mode

    def forward(self, x):

        # Ensure that x is a float tensors for unfold to work properly
        # Check if we need to apply padding
        if self.padding != (0,) * len(self.padding):
            x = tt.functional.Pad.apply(x, self.padding, self.padding_mode, self.value)

        # Use unfold to create the windows
        # Note: unfold only accepts int, convert stride and kernel_size to int if they are tuples
        windows = unfold(x.content, dimension=2, size=self.kernel_size[0], step=self.stride[0])

        for i in range(1, len(self.stride)):
            windows = unfold(windows, dimension=i + 2, size=self.kernel_size[i], step=self.stride[i])



        return (windows)


import numpy as np


def conv1d_texttensor(x: _TextTensor, weights, bias=None, stride=1, padding=0, dilation=1, groups=1):
    # Assuming padding is handled outside this function
    # Convert stride and kernel_size to int if they are tuples
    stride = stride[0] if isinstance(stride, tuple) else stride
    kernel_size = weights.shape[2]  # Assuming weights have the shape (out_channels, in_channels/group, kernel_size)

    # Use unfold to create the windows
    windows = unfold(x.content, dimension=2, size=kernel_size, step=stride)
    print(len(windows))
    # Placeholder for the convolution output
    conv_output = langtorch.zeros(windows.shape[:-2] + (weights.shape[0],)).content

    # Iterate through each output channel
    for out_channel in range(weights.shape[0]):
        # Assuming weights and bias are numpy arrays for simplicity
        kernel = weights[out_channel]
        b = bias[out_channel] if bias is not None else None

        # Iterate through each window
        for i in np.ndindex(windows.shape[:-2]):
            # Perform convolution on this window
            window = windows[i]
            conv_sum = Text()
            for k, w in zip(kernel.flatten(), window.flatten()):
                conv_sum = conv_sum + k * w

            # Add bias if provided
            if b is not None:
                conv_sum += b
            # Assign the convolution result (this is a placeholder operation, actual implementation may vary)
            conv_output[i + (out_channel,)] = conv_sum

    # The conv_output now contains the result of convolution in the form of a numpy array of objects
    # You need to convert this back to a TextTensor if necessary, depending on how you intend to use the results
    return conv_output

from langtorch import _TextTensor, Text

# Example TextTensor with 3 samples, each sample is 10 tokens long
example_content = [[Text(f"word{i}_{j}") for i in range(10)] for j in range(3)]
x = _TextTensor(example_content).reshape(3, 1, 10)
# Define example weights and bias for the convolution operation
# Assume we have 2 output channels, and we're using a kernel size of 3
weights = _TextTensor(np.arange(3).reshape(1, 1, 3)).content  # Simplified weights for demonstration
bias = _TextTensor(['bias', 'bias2']).content  # Simplified bias

# Assuming we have a function conv1d_texttensor defined as discussed
# Call the conv1d_texttensor function with the example TextTensor and convolution parameters
conv_output = conv1d_texttensor(x, weights, bias=bias, stride=1, padding=0, dilation=1, groups=1)

print(conv_output)