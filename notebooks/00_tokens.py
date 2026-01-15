import tiktoken

text = "Who is the PM of India?"

tokenizer = tiktoken.encoding_for_model(model_name="gpt-4")

tokenIds = tokenizer.encode(text)

print(tokenIds)

tokenToText = tokenizer.decode(tokenIds)

print(tokenToText)