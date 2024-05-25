## Experimenting

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "system", "content": "You are a helpful assistant."},
            abstract3,
            prompt,
            example_output,
            {"role": "user", "content": a[1]['ab']},
            prompt],
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=b[1]['body']['messages'],
)


o = json.loads(response.choices[0].message.content)
print(json.dumps(o, indent=2))


b = [
    {"custom_id": a[i]['pmid'], "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."}, abstract3, prompt, example_output, {"role": "user", "content": a[i]['ab']}, prompt]}} for i in range(len(a)) if 'ab' in a[i].keys()
]

with open("pubmed_batch.jsonl", "w") as f:
    for item in b:
        f.write(json.dumps(item) + "\n")

batch_input_file = client.files.create(
  file=open("pubmed_batch100.jsonl", "rb"),
  purpose="batch"
)

batch_input_file_id = batch_input_file.id

bid = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "nightly eval job"
    }
)

client.batches.retrieve(dict(bid)['id'])

import tiktoken

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text):
    tokens = encoding.encode(text)
    return len(tokens)

count_tokens(str(b[0])) * 1000





response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "You are a helpful assistant."},
            abstract3,
            prompt,
            example_output,
            {"role": "user", "content": bytes(a[i]['ab'], 'utf-8').decode('utf-8', 'ignore')},
            prompt],
)
