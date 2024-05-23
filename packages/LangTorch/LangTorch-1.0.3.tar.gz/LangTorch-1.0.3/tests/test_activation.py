import sys

sys.path.append("/src")
from langtorch import _TextTensor, TextModule
from langtorch.tt import Activation
from langtorch.api.call import chat, auth
import unittest


class TestActivationModules(unittest.TestCase):

    def test_openai_activation(self):
        tensor = _TextTensor(["Testing answer yes if you hear me", "Testing answer yes if you hear me"])
        activation = Activation(model="gpt-3.5-turbo-0613", T=0.)
        module = TextModule("{}. Say it two times", activation=activation)
        result = module(tensor)
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.
        self.assertEqual(tuple(str(m).lower().count("yes") for m in result.flat), (2,2))


if __name__ == "__main__":
    unittest.main()
