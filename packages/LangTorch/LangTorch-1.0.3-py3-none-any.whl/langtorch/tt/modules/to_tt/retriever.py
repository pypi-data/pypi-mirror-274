import torch

from textmodule import TextModule
from langtorch import TextTensor, Text


class Retriever(TextModule):
    def __init__(self, documents: TextTensor):
        super().__init__()
        self.documents = TextTensor(documents).view(-1)

    def forward(self, query: TextTensor, k: int = 5):
        cos_sim = torch.cosine_similarity(self.documents, query.reshape(1))
        return self.documents[cos_sim.topk(k)]


class RAG(TextModule):
    def __init__(self, documents: TextTensor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retriever = Retriever(documents)

    def forward(self, user_message: TextTensor, k: int = 5):
        retrieved_context = self.retriever(user_message, k) + "\n"
        user_message = user_message + "\nCONTEXT:\n" + retrieved_context.sum()
        return super().forward(user_message)

