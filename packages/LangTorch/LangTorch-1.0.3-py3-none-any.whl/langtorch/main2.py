from langtorch import TextTensor, Activation  # holds texts, instead of weights,  supports tensor operations
from langtorch import TextModule # are torch.nn modules working on TextTensors, perform prompt templating
import langtorch
import torch
from langtorch import Text
from langtorch import Session
# paper = Text.from_file("D:\langtorch\src\langtorch\conf\paper.md")
import os
import logging
# logging.basicConfig(level=logging.DEBUG)
# Example usage


with Session("test.yaml") as session:
    os.environ["GROQ_API_KEY"] = "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"
    # llm = Activation(model="llama3-70b-8192", provider="groq", T=1.2, max_tokens=350)
    llm = Activation(model="gpt-4o",  T=0., max_tokens=350)
    # llm = Activation(model="claude-3-opus-20240229", provider="anthropic", max_tokens=10)
    # chat = TextTensor({"user": input()})
    chat = TextTensor({"user": "make ascii art of donald trump"})

    # response = llm(chat)
    a = session.a
    b = (a).sum().item().loc["Para"]
    b = (a).loc["Para"]
    print([str(bb) for bb in b.flat])
    for i in range(3):
        print(b[i].item().items())


quit()

ensemble_llm = langtorch.OpenAI("gpt-3.5-turbo",
                      T=1.2, # High temperature to sample diverse completions
                      n = 4) # 5 completions for each entry



task = TextModule("Calculate the following: {} = ? Let's think step by step.", activation=ensemble_llm)
input_tensor = TextTensor("171*33")#, "4*20"])#, "123*45/10", "2**10*5"])
print(task(input_tensor).view(1,-1))
# paper = Text("""a
#
# b""", parse='md')
# paper = Text.from_file("D:\langtorch\src\langtorch\conf\paper.md")
# print(paper)
quit()
os.environ["GROQ_API_KEY"] = "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"
os.environ["ANTHROPIC_API_KEY"] = "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"
# llm = Activation(model="llama3-70b-8192",  provider="groq", T=1.2, max_tokens=350)
llm = Activation(model="claude-3-opus-20240229",  provider="anthropic", max_tokens=10)
# chat = TextTensor({"user": input()})
chat = TextTensor({"user": "Hi"})
while True:
    response = llm(chat)
    print(response)
    chat += Text({"user": input()})
