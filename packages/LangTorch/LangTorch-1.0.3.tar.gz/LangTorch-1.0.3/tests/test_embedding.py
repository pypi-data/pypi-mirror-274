from langtorch import _TextTensor, TextModule, OpenAI, Text
import os
import unittest
from langtorch import Session
import logging

# logging.basicConfig(level=logging.DEBUG)
# session = Session("embeddings_test_config.yaml")

# class TestEmbeddingModules(unittest.TestCase):
#     def test_openai_embedding(self):
#         tensor = TextTensor([str(i) for i in range(100)])
#         tensor.embed()
#         del tensor
#         tensor = TextTensor([str(i) for i in range(100)])
#         tensor.embed()
#
#         # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.
#         self.assertEqual(tuple(tensor.embedding.shape[:-1]), tensor.content.shape)


# if __name__ == "__main__":
#     unittest.main()


import torch

tensor1 = _TextTensor([[["Yes"], ["No"]]])
tensor2 = _TextTensor(["Yeah", "Nope", "Yup", "Non"])


class Retriever(TextModule):
    def __init__(self, documents: _TextTensor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.documents = _TextTensor(documents).view(-1)

    def forward(self, query: _TextTensor, k: int = 5):
        cos_sim = torch.cosine_similarity(self.documents, query.reshape(1))
        return self.documents[cos_sim.topk(k)]

paragraphs = Text.from_file("assets/paper.md").loc["Para"].to_tensor()
retriever = Retriever(paragraphs)

class RAG(TextModule):
    def __init__(self, documents: _TextTensor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retriever = Retriever(documents)

    def forward(self, user_message: _TextTensor, k: int = 5):
        retrieved_context = self.retriever(user_message, k) +"\n"
        user_message = user_message + "\nCONTEXT:\n" + retrieved_context.sum()
        return super().forward(user_message)

rag_chat = RAG(paragraphs,
                  prompt="Use the context to answer the following user query: ",
                  activation="gpt-3.5-turbo")

query = _TextTensor("What is the modal drift hypothesis?")
print(rag_chat(query))
# OUTPUTS:
# The modal drift hypothesis suggests that the inclusion of large language models
# in our information ecosystems could lead to a deterioration in quality due to the models'
# ability to produce statements that pass our plausibility checking without explicit intention
# to deceive, causing a discrepancy between perceived truthfulness and actual accuracy.


