The [Seekr Python Library](https://pypi.org/project/seekrflow/) is the official Python client for SeekrFlow's API platform, providing a convenient way for interacting with the REST APIs and enables easy integrations with Python 3.8+ applications with easy to use synchronous and asynchronous clients.

# Installation

> 🚧
> The library was rewritten in v1.0.0 released in April of 2024. There were significant changes made.

To install Seekr Python Library from PyPi, simply run:

```shell Shell
pip install --upgrade seekrai
```

## Setting up API Key

> 🚧 You will need to create an account with [Seekr.com](https://api.seekrflow.xyz/) to obtain a SeekrFlow API Key.

Once logged in to the SeekrFlow Playground, you can find available API keys in [this settings page](https://api.seekrflow.xyz/settings/api-keys).

### Setting environment variable

```shell
export SEEKRFLOW_API_KEY=xxxxx
```

### Using the client

```python
from seekrai import SeekrFlow

client = SeekrFlow(api_key="xxxxx")
```

This library contains both a python library and a CLI. We'll demonstrate how to use both below.

# Usage – Python Client

## Chat Completions

```python
import os
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))

response = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[{"role": "user", "content": "tell me about new york"}],
)
print(response.choices[0].message.content)
```

### Streaming

```python
import os
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))
stream = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[{"role": "user", "content": "tell me about new york"}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

### Async usage

```python
import os, asyncio
from seekrai import AsyncSeekrFlow

async_client = AsyncSeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))
messages = [
    "What are the top things to do in San Francisco?",
    "What country is Paris in?",
]


async def async_chat_completion(messages):
    async_client = AsyncSeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))
    tasks = [
        async_client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": message}],
        )
        for message in messages
    ]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.choices[0].message.content)


asyncio.run(async_chat_completion(messages))
```

## Completions

Completions are for code and language models shown [here](https://docs.seekrflow.ai/docs/inference-models). Below, a code model example is shown.

```python
import os
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))

response = client.completions.create(
    model="codellama/CodeLlama-34b-Python-hf",
    prompt="Write a Next.js component with TailwindCSS for a header component.",
)
print(response.choices[0].text)
```

### Streaming

```python
import os
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))
stream = client.completions.create(
    model="codellama/CodeLlama-34b-Python-hf",
    prompt="Write a Next.js component with TailwindCSS for a header component.",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

### Async usage

```python
import os, asyncio
from seekrai import AsyncSeekrFlow

async_client = AsyncSeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))
prompts = [
    "Write a Next.js component with TailwindCSS for a header component.",
    "Write a python function for the fibonacci sequence",
]


async def async_chat_completion(prompts):
    async_client = AsyncSeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))
    tasks = [
        async_client.completions.create(
            model="codellama/CodeLlama-34b-Python-hf",
            prompt=prompt,
        )
        for prompt in prompts
    ]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.choices[0].text)


asyncio.run(async_chat_completion(prompts))
```

## Image generation

```python
import os
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))

response = client.images.generate(
    prompt="space robots",
    model="stabilityai/stable-diffusion-xl-base-1.0",
    steps=10,
    n=4,
)
print(response.data[0].b64_json)
```

## Embeddings

```python
from typing import List
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))


def get_embeddings(texts: List[str], model: str) -> List[List[float]]:
    texts = [text.replace("\n", " ") for text in texts]
    outputs = client.embeddings.create(model=model, input=texts)
    return [outputs.data[i].embedding for i in range(len(texts))]


input_texts = ['Our solar system orbits the Milky Way galaxy at about 515,000 mph']
embeddings = get_embeddings(input_texts, model='seekrflowcomputer/m2-bert-80M-8k-retrieval')

print(embeddings)
```

## Files

The files API is used for fine-tuning and allows developers to upload data to fine-tune on. It also has several methods to list all files, retrive files, and delete files. Please refer to our fine-tuning docs [here](https://docs.seekrflow.ai/docs/fine-tuning-python).

```python
import os
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))

client.files.upload(file="somedata.jsonl")  # uploads a file
client.files.list()  # lists all uploaded files
client.files.retrieve(id="file-d0d318cb-b7d9-493a-bd70-1cfe089d3815")  # retrieves a specific file
client.files.retrieve_content(id="file-d0d318cb-b7d9-493a-bd70-1cfe089d3815")  # retrieves content of a specific file
client.files.delete(id="file-d0d318cb-b7d9-493a-bd70-1cfe089d3815")  # deletes a file
```

## Fine-tunes

The finetune API is used for fine-tuning and allows developers to create finetuning jobs. It also has several methods to list all jobs, retrive statuses and get checkpoints. Please refer to our fine-tuning docs [here](https://docs.seekrflow.ai/docs/fine-tuning-python).

```python
import os
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))

client.fine_tuning.create(
    training_file='file-d0d318cb-b7d9-493a-bd70-1cfe089d3815',
    model='mistralai/Mixtral-8x7B-Instruct-v0.1',
    n_epochs=3,
    n_checkpoints=1,
    batch_size=4,
    learning_rate=1e-5,
    suffix='my-demo-finetune',
    wandb_api_key='1a2b3c4d5e.......',
)
client.fine_tuning.list()  # lists all fine-tuned jobs
client.fine_tuning.retrieve(id="ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b")  # retrieves information on finetune event
client.fine_tuning.cancel(id="ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b")  # Cancels a fine-tuning job
client.fine_tuning.list_events(id="ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b")  # Lists events of a fine-tune job
client.fine_tuning.download(
    id="ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b")  # downloads compressed fine-tuned model or checkpoint to local disk
```

## Models

This lists all the models that SeekrFlow supports.

```python
import os
from seekrai import SeekrFlow

client = SeekrFlow(api_key=os.environ.get("SEEKRFLOW_API_KEY"))

models = client.models.list()

for model in models:
    print(model)
```

# Usage – CLI

## Chat Completions

```bash
seekrai chat.completions \
  --message "system" "You are a helpful assistant named SeekrFlow" \
  --message "user" "What is your name?" \
  --model mistralai/Mixtral-8x7B-Instruct-v0.1
```

The Chat Completions CLI enables streaming tokens to stdout by default. To disable streaming, use `--no-stream`.

## Completions

```bash
seekrai completions \
  "Large language models are " \
  --model mistralai/Mixtral-8x7B-v0.1 \
  --max-tokens 512 \
  --stop "."
```

The Completions CLI enables streaming tokens to stdout by default. To disable streaming, use `--no-stream`.

## Image Generations

```bash
seekrai images generate \
  "space robots" \
  --model stabilityai/stable-diffusion-xl-base-1.0 \
  --n 4
```

The image is opened in the default image viewer by default. To disable this, use `--no-show`.

## Files

```bash
# Help
seekrai files --help

# Check file
seekrai files check example.jsonl

# Upload file
seekrai files upload example.jsonl

# List files
seekrai files list

# Retrieve file metadata
seekrai files retrieve file-6f50f9d1-5b95-416c-9040-0799b2b4b894

# Retrieve file content
seekrai files retrieve-content file-6f50f9d1-5b95-416c-9040-0799b2b4b894

# Delete remote file
seekrai files delete file-6f50f9d1-5b95-416c-9040-0799b2b4b894
```

## Fine-tuning

```bash
# Help
seekrai fine-tuning --help

# Create fine-tune job
seekrai fine-tuning create \
  --model seekrflowcomputer/llama-2-7b-chat \
  --training-file file-711d8724-b3e3-4ae2-b516-94841958117d

# List fine-tune jobs
seekrai fine-tuning list

# Retrieve fine-tune job details
seekrai fine-tuning retrieve ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b

# List fine-tune job events
seekrai fine-tuning list-events ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b

# Cancel running job
seekrai fine-tuning cancel ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b

# Download fine-tuned model weights
seekrai fine-tuning download ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b
```

## Models

```bash
# Help
seekrai models --help

# List models
seekrai models list
```

## Contributing

Refer to the [Contributing Guide](CONTRIBUTING.md)
