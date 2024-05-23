import time

import unittest
import sys
sys.path.append("../src")

from langtorch.session import Session


from langtorch import _TextTensor
from langtorch.api import auth
from langtorch.tt import Activation
import logging

logging.basicConfig(level=logging.INFO)
# time the execution
start_time = time.time()


# class TestSessionAPI(unittest.TestCase):
#     def setUp(self):
#         # Create a sample config file for testing
#         self.config_path = "test_config.yaml"
#     def test_api_cache(self):
#         with Session(self.config_path) as session:
#             session.key1 = TextTensor(["test. Answer yes"]*3)
#             session.val1 = Activation()(session.key1)



    # def tearDown(self):
    #     # Cleanup: remove the test config file after each test
    #     os.remove(self.config_path)

# if __name__ == '__main__':
#     unittest.main()


session = Session("test_config.yaml", "test_session.hdf5")

out = Activation()(_TextTensor([[""]]))
# out2 = Activation(model = "gpt-4-1106-preview", T=1, max_tokens = 100)(TextTensor([["Write a joke"]]*2))
# out3 = Activation(model = "gpt-4-1106-preview", T=1, max_tokens = 100)(TextTensor([["Napisz listę rymów do Mieszko. Oddziel słowa jedynie spacją"]]*3))

print("GRAND SLAM\n", out )
# print("GRAND SLAM\n", out3  )

print(f"Execution time: {time.time()-start_time:.2f}")